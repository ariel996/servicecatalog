# Generated by Django 3.1.1 on 2020-09-30 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0078_auto_20200930_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
