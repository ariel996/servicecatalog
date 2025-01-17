# Generated by Django 3.0.3 on 2020-06-14 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_color',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='product_size',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='annonces',
            name='annonce_photo',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='uploads/announces'),
        ),
        migrations.CreateModel(
            name='Product_images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, null=True)),
                ('size', models.CharField(max_length=120, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='annonces.Products')),
            ],
        ),
    ]
