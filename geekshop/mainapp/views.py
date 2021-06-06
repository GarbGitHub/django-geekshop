from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory


def products(request, pk=None):
    title = 'каталог товаров'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            product = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': product,
        }

        return render(request, 'mainapp/products_list.html', context)

    product = Product.objects.all()

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': product
    }

    return render(request, 'mainapp/products.html', context)

    # links_menu = [
    #     {'href': 'products:products_all', 'name': 'все'},
    #     {'href': 'products:products_home', 'name': 'дом'},
    #     {'href': 'products:products_office', 'name': 'офис'},
    #     {'href': 'products:products_modern', 'name': 'модерн'},
    #     {'href': 'products:products_classic', 'name': 'классика'},
    # ]

    # context = {
    #     'title': title,
    #     'links_menu': links_menu,
    # }
    #
    # template = 'mainapp/products.html'
    #
    # if pk:
    #     obj = Product.objects.get(pk=pk)
    #     context['product'] = obj
    #     context['title'] = obj.name
    #     template = 'mainapp/product-card.html'
    #
    # return render(request, template, context=context)
