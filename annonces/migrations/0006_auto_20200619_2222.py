# Generated by Django 3.0.3 on 2020-06-19 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0005_auto_20200619_2220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annonces',
            old_name='category_id',
            new_name='category',
        ),
    ]
