# Generated by Django 3.2.3 on 2021-06-09 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210603_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_preview_1',
            field=models.ImageField(blank=True, upload_to='products_images', verbose_name='дополнительное изображение 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_preview_2',
            field=models.ImageField(blank=True, upload_to='products_images', verbose_name='дополнительное изображение 2'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_preview_3',
            field=models.ImageField(blank=True, upload_to='products_images', verbose_name='дополнительное изображение 3'),
        ),
    ]
