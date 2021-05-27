from django.shortcuts import render


def products(request):
    title = 'каталог товаров'
    links_menu = [
        {'href': 'mainapp:products_all', 'name': 'все'},
        {'href': 'mainapp:products_home', 'name': 'дом'},
        {'href': 'mainapp:products_office', 'name': 'офис'},
        {'href': 'mainapp:products_modern', 'name': 'модерн'},
        {'href': 'mainapp:products_classic', 'name': 'классика'},
    ]
    context = {
        'title': title,
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', context=context)
