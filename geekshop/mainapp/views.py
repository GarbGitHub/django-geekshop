from django.shortcuts import render
from .models import Product


def products(request, pk=None):
    title = 'каталог товаров'

    links_menu = [
        {'href': 'products:products_all', 'name': 'все'},
        {'href': 'products:products_home', 'name': 'дом'},
        {'href': 'products:products_office', 'name': 'офис'},
        {'href': 'products:products_modern', 'name': 'модерн'},
        {'href': 'products:products_classic', 'name': 'классика'},
    ]

    context = {
        'title': title,
        'links_menu': links_menu,
    }

    template = 'mainapp/products.html'

    if pk:
        context['product'] = Product.objects.get(pk=pk)
        template = 'mainapp/product-card.html'

    return render(request, template, context=context)
