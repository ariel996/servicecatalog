# Generated by Django 3.0.3 on 2020-06-19 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0003_auto_20200618_2018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annonces',
            old_name='category',
            new_name='category_id',
        ),
    ]
