# Generated by Django 3.2.4 on 2021-06-26 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timewebapp', '0045_alter_settingsmodel_first_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timewebmodel',
            old_name='dif_assign',
            new_name='blue_line_start',
        ),
    ]