# Generated by Django 4.2 on 2023-04-25 18:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="registerhackathon",
            old_name="name",
            new_name="submission_name",
        ),
    ]
