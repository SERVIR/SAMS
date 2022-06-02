# Generated by Django 3.2.4 on 2022-05-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_application_developers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the application component (indicate version if relevant)', max_length=250)),
                ('description', models.TextField(blank=True, help_text='Further details for the application component')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='application_components',
            field=models.ManyToManyField(blank=True, to='app.ApplicationComponent'),
        ),
    ]