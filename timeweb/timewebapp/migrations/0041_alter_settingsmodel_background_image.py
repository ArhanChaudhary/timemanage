# Generated by Django 3.2.4 on 2021-06-16 06:48

from django.db import migrations, models
import timewebapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0040_settingsmodel_background_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingsmodel',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to=timewebapp.models.create_path),
        ),
    ]