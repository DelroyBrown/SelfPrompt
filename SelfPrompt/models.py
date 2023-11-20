from django.db import models


class ArtPrompt(models.Model):
    prompt = models.TextField()
    style_id = models.CharField(max_length=50)
    art_style = models.CharField(max_length=50)
    aspect_ratio = models.CharField(max_length=10)
    high_res = models.BooleanField(default=False)
    generated_image = models.ImageField(upload_to="generated_images/")

    def __str__(self):
        return self.prompt
