# Generated by Django 4.0.4 on 2022-06-03 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_application_incomplete_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='photo',
            field=models.ImageField(blank=True, help_text='Square image, minimum 150px X 150px', null=True, upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='scientist',
            name='photo',
            field=models.ImageField(blank=True, help_text='Square image, minimum 150px X 150px', null=True, upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='servicearea',
            name='service_catalog_url',
            field=models.URLField(blank=True, help_text='Reference to the SERVIR Service catalog'),
        ),
    ]