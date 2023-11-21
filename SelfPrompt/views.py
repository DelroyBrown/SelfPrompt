import os
import requests
import logging
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
from .models import ArtPrompt

logger = logging.getLogger(__name__)


def render_form(request):
    return render(request, "prompt_form.html")


@require_http_methods(["POST"])
def home(request):
    url = "https://api.vyro.ai/v1/imagine/api/generations"

    not_token = os.getenv('PROMPT_KEY')
    headers = {
        "Authorization": f"Bearer {not_token}"
    }

    # Get POST data
    full_name = request.POST.get("full_name")
    prompt_text = request.POST.get("prompt")
    style_id = request.POST.get("style_id")
    art_style = request.POST.get("art_style")
    aspect_ratio = request.POST.get("aspect_ratio")
    high_res = request.POST.get("high_res_results") == "1"
    seed = request.POST.get("seed")
    combined_style = f"{style_id}:{art_style}"

    seed = random.randint(1, 10000000)
    payload = {
        "full_name": (None, full_name),
        "prompt": (None, prompt_text),
        "style_id": (None, combined_style),
        "aspect_ratio": (None, aspect_ratio),
        "high_res_results": (None, request.POST.get("high_res_results")),
        "seed": (None, str(seed)),
    }
    print(payload)

    response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        art_prompt = ArtPrompt(
            full_name=full_name,
            prompt=prompt_text,
            style_id=style_id,
            art_style=art_style,
            aspect_ratio=aspect_ratio,
            high_res=high_res,
            seed=seed,
            generated_image=ContentFile(response.content, name=f"{prompt_text}.png"),
            submission_date=timezone.now().strftime("%d/%m/%y"),
        )
        art_prompt.save()

        # Construct the image link
        image_link = request.build_absolute_uri(art_prompt.generated_image.url)

        context = {
            "image_generated": True,
            "image_link": image_link,
            "art_prompt_id": art_prompt.id,
        }
        return render(request, "image_choices_template.html", context)
    else:
        return HttpResponse("API request failed", status=response.status_code)


@require_http_methods(["POST"])
def save_image(request):
    art_prompt_id = request.POST.get("art_prompt_id")
    frame_option = request.POST.get("frame_option", "unframed")
    frame_size = request.POST.get("frame_size", "30x30")  # Default value if none provided

    art_prompt = ArtPrompt.objects.get(id=art_prompt_id)
    art_prompt.frame_option = frame_option
    art_prompt.frame_size = frame_size if frame_option != "unframed" else "Not applicable"
    art_prompt.save()

    # Construct the image link
    image_link = request.build_absolute_uri(art_prompt.generated_image.url)

    # Mapping dictionaries
    MODEL_ID_CHOICES = {
        "33": "PromptAi V5",
        "34": "Anime V5",
        "32": "PromptAi V4.1",
        "31": "PromptAi V4 (Creative)",
        "30": "PromptAi V4",
        "28": "PromptAi V3",
        "27": "PromptAi V1",
        "29": "Realistic",
        "21": "Anime",
        "26": "Portrait",
        "122": "SDXL 1.0",
    }

    ART_STYLE_CHOICES = {
        "63": "Sticker",
        "89": "Fantasy",
        "55": "Render",
        "78": "Vibrant",
        "91": "Woolitize",
        "12": "Studio Ghibli",
        "74": "Van Gogh",
        "82": "Polaroid",
        "40": "Rococco",
        "56": "Coloring Book",
        "48": "Samurai",
        "8": "Minecraft",
        "49": "Aquatic",
        "44": "Firebender",
        "33": "Neo fauvism",
        "52": "Illustration",
        "7": "Marble",
        "57": "PaperCut Style",
        "88": "Rennaisance",
        "11": "GTA",
        "15": "Product Photography",
        "32": "Clip Art",
        "37": "Neon",
        "43": "Waterbender",
        "53": "Painting",
        "14": "Stained Glass",
        "19": "Gothic",
        "21": "Avatar",
        "79": "Mystical",
        "69": "Retro",
        "31": "Chromatic",
        "51": "Abstract Cityscape",
        "84": "Sketch",
        "59": "Anime V2",
        "68": "Scatter",
        "66": "Architecture",
        "60": "Pixel Art",
        "61": "Comic V2",
        "41": "Haunted",
        "10": "Macro Photography",
        "67": "Glass Art",
        "73": "Salvador Dali",
        "6": "Cosmic",
        "18": "Graffiti",
        "58": "Knolling Case",
        "29": "Pop Art II",
        "20": "Rainbow",
        "72": "Japanese Art",
        "35": "Shamrock Fantasy",
        "13": "Dystopian",
        "70": "Poster Art",
        "26": "Medieval",
        "77": "Poly Art",
        "25": "Euphoric",
        "50": "Vibrant Viking",
        "42": "Logo",
        "85": "Comic Book",
        "36": "Abstract Vibrant",
        "65": "Landscape",
        "92": "Cinematic Render",
        "45": "Kawaii Chibi",
        "24": "Claymation",
        "27": "Origami",
        "30": "Pattern",
        "64": "Cyberpunk",
        "71": "Ink",
        "47": "Elven",
        "34": "Amazonian",
        "76": "Retrowave",
        "28": "Pop Art",
        "38": "Cubism",
        "54": "Icon",
        "9": "Disney",
        "75": "Steampunk",
        "81": "Futuristic",
        "46": "Forestpunk",
        "23": "Candyland",
    }

    model_name = MODEL_ID_CHOICES.get(art_prompt.style_id, "Unknown Style")
    art_style_name = ART_STYLE_CHOICES.get(art_prompt.art_style, "Unknown Art Style")

    # Format the submission date
    formatted_date = art_prompt.submission_date.strftime("%d/%m/%Y")

    # Construct the email message
    email_message = (
        f"Full Name: {art_prompt.full_name}\n"
        f"Prompt Text: {art_prompt.prompt}\n"
        f"Model: {model_name}\n"
        f"Style: {art_style_name}\n"
        f"Aspect Ratio: {art_prompt.aspect_ratio}\n"
        f"High Resolution: {'Yes' if art_prompt.high_res else 'No'}\n"
        f"Seed: {art_prompt.seed}\n"
        f"Generated Image Link: {image_link}\n"
        f"Frame Option: {frame_option}\n"
        f"Frame/Image Size: {frame_size}\n"
        f"Submission Date: {formatted_date}"
    )

    # Send the email
    send_mail(
        f"New Prompt from {art_prompt.full_name}. {formatted_date}",
        email_message,
        settings.EMAIL_HOST_USER,
        ["promptai.dbrown@gmail.com"],
        fail_silently=False,
    )

    return HttpResponse("Image saved and email sent.")
