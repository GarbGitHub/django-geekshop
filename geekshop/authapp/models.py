from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    # Для поля выбора select
    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    # Для создания связи «один-к-одному» используем поле models.OneToOneField.
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    vk_profile = models.CharField(verbose_name='профиль ВК', max_length=128, blank=True)
    vk_user_avatar = models.CharField(verbose_name='фото вк', max_length=256, blank=True)
    language = models.CharField(verbose_name='язык', max_length=128, blank=True)


    @receiver(post_save, sender=ShopUser)
    # сигналом является сохранение (post_save) объекта модели ShopUser (sender=ShopUser).
    def create_user_profile(sender, instance, created, **kwargs):
        """
        Механизм синхронных действий со связанной моделью, при создании нового пользователя ShopUser, создать профиль
        :param instance: конкретный объект, на котором сработал сигнал
        :param created: сигнал создания объекта
        :param kwargs:
        :return:
        """
        if created:  # если создан впервые
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        """Сохранение профиля"""
        instance.shopuserprofile.save()
