from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from adminapp.forms import ShopUserRegisterForm, ProductCategoryEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, redirect
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def users(request, **kwargs):
    title = 'пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list,
        'icon': 'bx-user',
    }

    if len(kwargs) > 0:
        for key, value in kwargs.items():
            context[key]: value

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
            # return HttpResponseRedirect(reverse('admin_staff:users', kwargs={'alert': 'Пользователь добавлен'}))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form,
        'icon': 'bx-user-plus',
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    title = f'пользователь: {edit_user.username}'

    if request.method == 'POST':
        edit_form = ShopUserRegisterForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserRegisterForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form,
        'icon': 'bx-edit',
        'edit_user': edit_user
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    title = f'удалить: {user.username}'

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user,
        'icon': 'bx-user-x',
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'категории товаров'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list,
        'icon': 'bx-category',
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'создание категории'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    else:
        category_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'update_form': category_form,
        'icon': 'bx-category',
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    title = f'категория: {edit_category.name}'

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'update_form': edit_form,
        'icon': 'bx-edit',
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_to_delete = get_object_or_404(ProductCategory, pk=pk)
    title = f'удалить: {category_to_delete.name}'

    if request.method == 'POST':
        category_to_delete.is_active = False
        category_to_delete.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category_to_delete,
        'icon': 'bx-user-x',
    }

    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass
