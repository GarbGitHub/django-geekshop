from django.urls import path
from .views import products
import mainapp.views as mainapp

app_name = 'mainapp'  # для работы 'namespace=' в geekshop/urls.py

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:pk>/', products, name='category'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),
]
