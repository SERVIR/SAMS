# Generated by Django 4.2.1 on 2024-05-29 19:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0027_feedback"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeneralFeedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feedback_entry", models.TextField()),
                (
                    "date",
                    models.DateField(
                        blank=True,
                        default=datetime.date.today,
                        help_text="Date feedback reported",
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("resolved", models.BooleanField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="generalfeedback",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
