# Generated by Django 3.2.3 on 2021-06-03 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210531_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': ('продукт',), 'verbose_name_plural': 'продукты'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': ('категория',), 'verbose_name_plural': 'категории'},
        ),
    ]
