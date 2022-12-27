# Generated by Django 4.0.4 on 2022-12-27 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_link_application_related_links'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='related_links',
        ),
        migrations.AddField(
            model_name='link',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.application'),
        ),
    ]
