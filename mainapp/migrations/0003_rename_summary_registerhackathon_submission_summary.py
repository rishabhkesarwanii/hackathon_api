# Generated by Django 4.2 on 2023-04-25 18:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0002_rename_name_registerhackathon_submission_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="registerhackathon",
            old_name="summary",
            new_name="submission_summary",
        ),
    ]