# Generated by Django 3.0.7 on 2020-07-27 16:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annonces', '0046_auto_20200726_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonces',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]