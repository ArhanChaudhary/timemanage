# Generated by Django 3.1.3 on 2021-01-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0008_remove_timewebmodel_nwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timewebmodel',
            name='x',
            field=models.DateField(null=True),
        ),
    ]