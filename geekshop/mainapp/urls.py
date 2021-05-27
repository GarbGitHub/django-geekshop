from django.urls import path
from . import views

app_name = 'mainapp'  # для работы 'namespace=' в geekshop/urls.py

urlpatterns = [
    path('', views.products, name='index'),
    path('products_all/', views.products, name='products_all'),
    path('products_home/', views.products, name='products_home'),
    path('products_office/', views.products, name='products_office'),
    path('products_modern/', views.products, name='products_modern'),
    path('products_classic/', views.products, name='products_classic'),
]
