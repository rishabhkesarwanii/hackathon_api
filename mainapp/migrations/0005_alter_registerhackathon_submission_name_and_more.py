# Generated by Django 4.2 on 2023-04-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0004_alter_registerhackathon_submission_link_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registerhackathon",
            name="submission_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="registerhackathon",
            name="submission_summary",
            field=models.TextField(blank=True, null=True),
        ),
    ]
