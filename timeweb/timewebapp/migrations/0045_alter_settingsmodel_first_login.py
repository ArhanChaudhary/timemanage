# Generated by Django 3.2.4 on 2021-06-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0044_alter_settingsmodel_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingsmodel',
            name='first_login',
            field=models.BooleanField(default=True, verbose_name='Enable Tutorial'),
        ),
    ]