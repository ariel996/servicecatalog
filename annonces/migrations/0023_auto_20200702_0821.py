# Generated by Django 3.0.3 on 2020-07-02 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0022_auto_20200702_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annonces',
            old_name='ville',
            new_name='villes',
        ),
    ]
