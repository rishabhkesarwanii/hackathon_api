# Generated by Django 4.2 on 2023-04-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0010_alter_hackathon_background_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hackathon",
            name="background_image",
            field=models.ImageField(upload_to="hackathons/background_images/"),
        ),
        migrations.AlterField(
            model_name="hackathon",
            name="hackathon_image",
            field=models.ImageField(upload_to="hackathons/hackathon_images/"),
        ),
        migrations.AlterField(
            model_name="registerhackathon",
            name="submission_file",
            field=models.FileField(
                blank=True, null=True, upload_to="hackathons/submissions/file"
            ),
        ),
        migrations.AlterField(
            model_name="registerhackathon",
            name="submission_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="hackathons/submissions/image"
            ),
        ),
    ]
