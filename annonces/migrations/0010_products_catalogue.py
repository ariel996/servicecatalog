# Generated by Django 3.0.3 on 2020-06-25 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0009_catalogue_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='catalogue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='annonces.Catalogue'),
        ),
    ]
