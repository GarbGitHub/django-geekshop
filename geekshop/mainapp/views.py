from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }
    print(request.user)

    return render(request, 'mainapp/product.html', content)


def products(request, pk=None, page=1):
    title = 'Каталог товаров '
    links_menu = ProductCategory.objects.filter(is_active=True)

    # basket = []
    #
    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter(user=request.user)

    # Категории товаров
    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            title = f'Категория: "Все"'
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            title = f'Категория: "{category.name}"'  # title, H2 Категория: "Дом"

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products.html', context)

    # Главная страница каталога товаров
    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context)
