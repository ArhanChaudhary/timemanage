# Generated by Django 3.1.8 on 2021-04-17 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0010_auto_20210410_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settingsmodel',
            old_name='def_nwd',
            new_name='defnwd',
        ),
    ]
