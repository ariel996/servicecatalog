# Generated by Django 3.1 on 2020-08-09 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0052_profile_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
