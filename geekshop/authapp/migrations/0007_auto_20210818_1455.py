# Generated by Django 3.2.3 on 2021-08-18 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20210818_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='vk_user_avatar',
            field=models.CharField(blank=True, max_length=256, verbose_name='фото вк'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 20, 14, 55, 11, 327951)),
        ),
    ]
