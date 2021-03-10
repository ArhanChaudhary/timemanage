# Generated by Django 3.1.3 on 2021-03-10 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0013_auto_20210309_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timewebmodel',
            name='skew_ratio',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=17, null=True, verbose_name='Enter the Estimated amount of Time to complete each Unit of Work in Minutes'),
        ),
    ]