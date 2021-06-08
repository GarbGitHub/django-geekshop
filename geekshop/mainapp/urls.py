from django.urls import path
from .views import products

app_name = 'mainapp'  # для работы 'namespace=' в geekshop/urls.py

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:pk>/', products, name='category'),
]
