# Generated by Django 3.1.3 on 2021-01-26 04:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0012_auto_20210125_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timewebmodel',
            name='adone',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='dif_assign',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='dynamic_start',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='file_sel',
            field=models.CharField(max_length=40, verbose_name='Name: '),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='funct_round',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='min_work_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='nwd',
            field=models.CharField(blank=True, choices=[('0', 'SUNDAY'), ('1', 'MONDAY'), ('2', 'TUESDAY'), ('3', 'WEDNESDAY'), ('4', 'THURSDAY'), ('5', 'FRIDAY'), ('6', 'SATURDAY')], max_length=2),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='remainder_mode',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='total_mode',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='timewebmodel',
            name='unit',
            field=models.CharField(blank=True, default='Minute', max_length=40),
        ),
    ]