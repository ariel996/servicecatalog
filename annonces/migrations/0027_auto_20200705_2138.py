# Generated by Django 3.0.3 on 2020-07-05 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0026_messages_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='prestataire',
            new_name='client',
        ),
    ]
