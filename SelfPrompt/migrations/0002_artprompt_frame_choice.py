# Generated by Django 4.2.7 on 2023-11-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SelfPrompt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artprompt',
            name='frame_choice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]