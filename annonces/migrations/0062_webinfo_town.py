# Generated by Django 3.1 on 2020-08-28 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0061_webinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinfo',
            name='town',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
