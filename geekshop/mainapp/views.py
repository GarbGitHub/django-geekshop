from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory


def products(request, pk=None):
    title = 'Каталог товаров '
    links_menu = ProductCategory.objects.all()
    basket = []
    count_products = 0
    total_price = 0

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

        # Подсчет количества и общей суммы №7*
        for item in basket:
            count_products += item.quantity
            total_price += (item.product.price * item.quantity)

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
            'count_products': count_products,
            'total_price': total_price,

        }

        return render(request, 'mainapp/products.html', context)

    product = Product.objects.all()
    context = {
        'title': title,
        'links_menu': links_menu,
        'products': product,
        'basket': basket,
        'count_products': count_products,
        'total_price': total_price,
    }

    return render(request, 'mainapp/products.html', context)
