from django.contrib import admin

# Register your models here.
from ordersapp.models import Order


@admin.register(Order)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'status')
    list_filter = ('created', 'user')

