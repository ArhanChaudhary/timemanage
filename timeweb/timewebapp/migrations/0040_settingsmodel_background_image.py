# Generated by Django 3.2.4 on 2021-06-14 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0039_auto_20210531_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingsmodel',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
