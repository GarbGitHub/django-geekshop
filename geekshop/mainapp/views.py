import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
from random import randint


def get_basket(user):
    """
    Создание пользовательской корзины продуктов
    :param user:
    :return: корзина пользователя
    """
    if user.is_authenticated:
        return Basket.objects.filter(user=user) if user.is_authenticated else []


def get_hot_product():
    """
    Генерация случайного продукта
    :return: случайный продукт
    """
    products = Product.objects.all()
    # return random.sample(list(products), 1)[0]  # создан лишний объект list
    return products[randint(0, len(products) - 1)]


def get_same_product(hot_product):
    """
    Получение случайных продуктов из категории открытого горячего продукта
    :param hot_product: горячий продукт
    :return: список продуктов
    """
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    title = 'Каталог товаров '
    links_menu = ProductCategory.objects.all()
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            product = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product = Product.objects.filter(category__pk=pk).order_by('price')
            title = f'Категория: "{category.name}"'  # title, H2 Категория: "Дом"

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': product,
            'basket': basket,
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'basket': basket,
        'hot_product': hot_product,
        'same_product': same_products,
    }

    return render(request, 'mainapp/products.html', context)
