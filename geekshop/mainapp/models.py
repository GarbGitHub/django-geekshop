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
        return f'{self.name} id: {self.id} -- {self.created}'

    class Meta:
        verbose_name = 'категория',
        verbose_name_plural = 'категории'


# python manage.py makemigrations
# python manage.py migrate

class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        on_delete=models.CASCADE)

    name = models.CharField(
        verbose_name='название товара',
        max_length=128
    )

    image = models.ImageField(  # pip install Pillow
        verbose_name='изображение товара',
        upload_to='products_images',
        blank=True
    )

    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=256,
        blank=True
    )

    description = models.TextField(
        verbose_name='описание товара',
        blank=True
    )

    price = models.DecimalField(
        verbose_name='цена товара',
        max_digits=8,
        decimal_places=2,
        default=0
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество на складе',
        default=0
    )

    created = models.DateTimeField(auto_now_add=True)

    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} id: {self.id} -- {self.created}'

    class Meta:
        verbose_name = 'продукт',
        verbose_name_plural = 'продукты'
