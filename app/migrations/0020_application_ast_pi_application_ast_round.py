# Generated by Django 4.2.1 on 2024-04-17 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0019_remove_application_primary_developer"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="ast_pi",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Scientist who is/was the PI when the application was developed",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="PI_Scientist",
                to="app.scientist",
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="ast_round",
            field=models.IntegerField(
                blank=True,
                default=None,
                help_text="AST round they were involved with when the app was created",
                null=True,
            ),
        ),
    ]