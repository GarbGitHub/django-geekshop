from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    title = 'geekshop'
    products = Product.objects.filter(is_active=True, category__is_active=True)[:4]
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]

    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
    }
    return render(request, 'geekshop/contact.html', context=context)
