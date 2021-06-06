from django.urls import path
from .views import products

app_name = 'mainapp'  # для работы 'namespace=' в geekshop/urls.py

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:pk>/', products, name='category'),
    # path('product/<int:pk>', products, name='product'),
    # path('products_all/', products, name='products_all'),
    # path('products_home/', products, name='products_home'),
    # path('products_office/', products, name='products_office'),
    # path('products_modern/', products, name='products_modern'),
    # path('products_classic/', products, name='products_classic'),
]
