# Generated by Django 3.0.3 on 2020-06-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0014_product_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonces',
            name='ville',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]