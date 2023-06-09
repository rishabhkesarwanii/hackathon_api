# Generated by Django 4.2 on 2023-04-26 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0005_alter_registerhackathon_submission_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registerhackathon",
            name="submission_media",
        ),
        migrations.AddField(
            model_name="registerhackathon",
            name="submission_file",
            field=models.FileField(
                blank=True, null=True, upload_to="hackathons/submissions/file"
            ),
        ),
        migrations.AddField(
            model_name="registerhackathon",
            name="submission_image",
            field=models.FileField(
                blank=True, null=True, upload_to="hackathons/submissions/image"
            ),
        ),
    ]
