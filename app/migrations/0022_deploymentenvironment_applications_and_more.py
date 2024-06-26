# Generated by Django 4.2.1 on 2024-05-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0021_region_accronym"),
    ]

    operations = [
        migrations.AddField(
            model_name="deploymentenvironment",
            name="applications",
            field=models.ManyToManyField(blank=True, to="app.application"),
        ),
        migrations.RemoveField(
            model_name="application",
            name="deployment_environment",
        ),
        migrations.AddField(
            model_name="application",
            name="deployment_environment",
            field=models.ManyToManyField(blank=True, to="app.deploymentenvironment"),
        ),
    ]
