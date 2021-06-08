from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    title = 'Корзина покупок'
    basket = []
    count_products = 0
    total_price = 0

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

        # Подсчет количества и общей суммы №7*
        for item in basket:
            count_products += item.quantity
            total_price += (item.product.price * item.quantity)

    context = {
        'title': title,
        'basket': basket,
        'count_products': count_products,
        'total_price': total_price,
    }
    return render(request, 'basketapp/basket.html', context=context)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    pass
