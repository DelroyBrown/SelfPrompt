from django.contrib import admin
from .models import ArtPrompt

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

STYLE_ID_CHOICES = {
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


class ArtPromptAdmin(admin.ModelAdmin):
    def get_model_name(self, obj):
        return MODEL_ID_CHOICES.get(obj.style_id, "Unknown Model")

    get_model_name.short_description = "Model Name"

    def get_style_name(self, obj):
        return STYLE_ID_CHOICES.get(obj.art_style, "Unknown Style")

    get_style_name.short_description = "Style Name"

    list_display = (
        "prompt",
        "get_model_name",
        "get_style_name",
        "aspect_ratio",
        "high_res",
        "seed",
    )

    readonly_fields = (
        "full_name",
        "prompt",
        "get_model_name",
        "get_style_name",
        "aspect_ratio",
        "high_res",
        "seed",
    )


admin.site.register(ArtPrompt, ArtPromptAdmin)
