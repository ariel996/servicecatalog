# Generated by Django 3.0.7 on 2020-07-20 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0034_contacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='villes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='villes',
            name='region_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='villes',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
