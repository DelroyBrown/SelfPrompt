from django.utils import timezone
from django.db import models


class ArtPrompt(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True, default='')
    prompt = models.TextField()
    style_id = models.CharField(max_length=50)
    art_style = models.CharField(max_length=50)
    aspect_ratio = models.CharField(max_length=10)
    high_res = models.BooleanField(default=False)
    seed = models.CharField(max_length=50, default='', blank=True, null=True)
    generated_image = models.ImageField(upload_to="generated_images/")
    submission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.prompt
