from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя',
                            max_length=64,
                            unique=True)

    description = models.TextField(verbose_name='описание',
                                   blank=True,  # Не обязательное поле для заполнения
                                   null=True)

    created = models.DateTimeField(auto_now_add=True)

    update = models.DateTimeField(auto_now=True)

    # decimal = models.DecimalField(
    #     max_digits=10,  # максимальное число цифр
    #     decimal_places=223  # число знаков после запятой
    # )

    def __str__(self):
        return self.name

# python manage.py makemigrations
