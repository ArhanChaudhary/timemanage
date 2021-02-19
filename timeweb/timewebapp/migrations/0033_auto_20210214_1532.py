# Generated by Django 3.1.3 on 2021-02-14 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0032_auto_20210214_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timewebmodel',
            name='file_sel',
            field=models.CharField(error_messages={'required': 'This field cannot be a space', 'unique': 'An assignment with this name already exists'}, max_length=100, unique=True, verbose_name='Enter the Name of this Assignment'),
        ),
    ]