# Generated by Django 3.1.1 on 2020-09-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0074_auto_20200929_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='service_amount',
            field=models.CharField(max_length=100, null=True),
        ),
    ]