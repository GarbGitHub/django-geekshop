from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')

    # Ключ подтверждения создается с помощью хеш-функции при регистрации пользователя
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))  # Срок действия ключа

    def is_activation_key_expired(self):
        """
        Метод выполняет проверку актуальности ключа.
        :return: True or False
        """
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
