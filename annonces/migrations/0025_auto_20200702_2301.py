# Generated by Django 3.0.3 on 2020-07-02 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0024_auto_20200702_2242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='client',
            new_name='prestataire',
        ),
    ]
