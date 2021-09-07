from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Product, ProductCategory
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_hot_product():
    """
    Генерация случайного продукта
    :return: случайный продукт
    """
    products = Product.objects.filter(is_active=True).all()
    # return random.sample(list(products), 1)[0]  # создан лишний объект list

    return products[randint(0, len(products) - 1)]


def get_same_product(hot_product):
    """
    Получение случайных продуктов из категории открытого горячего продукта
    :param hot_product: горячий продукт
    :return: список продуктов
    """
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    # same_products = Product.objects.filter(is_active=True).select_relatede('category').exclude(pk=hot_product.pk)[:3]

    return same_products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['title'] = context.get(self, self.object.name)
        context['links_menu'] = ProductCategory.objects.filter(is_active=True)
        return self.render_to_response(context)


# class ProductListView(ListView):
#     model = Product
#     template_name = 'mainapp/products.html'
#     context_object_name = 'products'
#
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         context = self.get_context_data()
#         context['basket'] = get_basket(request.user)
#         return self.render_to_response(context)
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


def products(request, pk=None, page=1):
    title = 'Каталог товаров '
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.filter(
                is_active=True,
                category__is_active=True
            ).order_by('price')
            title = f'Категория: "Все"'
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True).order_by(
                'price')
            title = f'Категория: "{category.name}"'  # title, H2 Категория: "Дом"

        paginator = Paginator(products, 3)

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
        }

        return render(request, 'mainapp/products.html', context)

    # Главная страница каталога товаров
    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context)
