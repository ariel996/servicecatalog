# Generated by Django 3.1 on 2020-08-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0063_webinfo_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinfo',
            name='webname',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
