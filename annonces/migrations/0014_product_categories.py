# Generated by Django 3.0.3 on 2020-06-26 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0013_auto_20200626_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]