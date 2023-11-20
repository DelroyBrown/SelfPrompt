import requests
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
from .models import ArtPrompt

logger = logging.getLogger(__name__)


def render_form(request):
    return render(request, "prompt_form.html")


@require_http_methods(["POST"])
def home(request):
    url = "https://api.vyro.ai/v1/imagine/api/generations"

    headers = {"Authorization": "Bearer vk-kagDFeSv2d7lPsITfj1OGoCFrOcrEbHQ3P6ImmZSCOz3Vu"}

    # Get POST data
    prompt_text = request.POST.get("prompt")
    style_id = request.POST.get("style_id")
    art_style = request.POST.get("art_style")
    aspect_ratio = request.POST.get("aspect_ratio")
    high_res = request.POST.get("high_res_results") == "1"

    combined_style = f"{style_id}:{art_style}"

    payload = {
        "prompt": (None, prompt_text),
        "style_id": (None, combined_style),
        "aspect_ratio": (None, aspect_ratio),
        "high_res_results": (None, request.POST.get("high_res_results")),
    }

    response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        art_prompt = ArtPrompt(
            prompt=prompt_text,
            style_id=style_id,
            art_style=art_style,
            aspect_ratio=aspect_ratio,
            high_res=high_res,
            # Wrap the image data in a ContentFile
            generated_image=ContentFile(response.content, name="generated_image.jpg")  # Or use a dynamic name
        )
        art_prompt.save()

        # Return the binary content directly
        return HttpResponse(response.content, content_type="image/jpeg")
    else:
        # Handle non-200 responses
        return HttpResponse("API request failed", status=response.status_code)
