# Generated by Django 3.0.3 on 2020-07-06 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0028_messages_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogue',
            name='date_created',
        ),
    ]
