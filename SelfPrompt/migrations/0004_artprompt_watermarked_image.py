# Generated by Django 4.2.7 on 2023-11-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SelfPrompt', '0003_artprompt_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='artprompt',
            name='watermarked_image',
            field=models.ImageField(blank=True, null=True, upload_to='watermarked_images/'),
        ),
    ]
