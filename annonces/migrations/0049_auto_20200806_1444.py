# Generated by Django 3.1 on 2020-08-06 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0048_comments_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_subcategories',
            name='category',
        ),
        migrations.DeleteModel(
            name='Product_categories',
        ),
        migrations.DeleteModel(
            name='Product_subcategories',
        ),
    ]
