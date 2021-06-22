from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserRegisterForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    ordering = '-is_active', '-is_staff'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icon'] = 'bx-user'
        context['title'] = 'Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
            # return redirect('admin_staff:users', kwargs={'alert': 'Успешно добавлен'})

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form,
        'icon': 'bx-user-plus',
    }

    return render(request, 'adminapp/user_update.html', context)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    context_object_name = 'edit_user'

    def get_form(self, form_class=ShopUserRegisterForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('adminapp:user_update', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f'пользователь: {context.get(self, self.object.username)}'
        context['title'] = title
        context['icon'] = 'bx-edit'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    # fields = '__all__'  # get_form()

    def get_form(self, form_class=ProductCategoryEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, *args, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['icon'] = 'bx-category'
        context['title'] = f'Создание категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    ordering = '-is_active'
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['icon'] = 'bx-cart'
        context['title'] = f'категории товаров'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_form(self, form_class=ProductCategoryEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'категория: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')
    context_object_name = 'category_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'удалить категорию: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    ordering = '-is_active'
    paginate_by = 2

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, *args, object_lists=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context['icon'] = 'bx-cart'
        context['title'] = f'товары категории "{category.name}"'
        context['category'] = category
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# class ProductCreateView(CreateView):
#     model = Product
#     template_name = 'adminapp/product_update.html'
#     success_url = reverse_lazy('admin_staff:categories')
#     # initial = {}
#     fields = '__all__'  # get_form()
#
#     # def get_form(self, form_class=ProductEditForm):
#     #     """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
#     #     return form_class(**self.get_form_kwargs())
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductCreateView, self).get_context_data(**kwargs)
#         context['icon'] = 'bx-category'
#         context['title'] = f'Добавить новый товар'
#         return context
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'Добавить новый товар'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
    else:
        # элемент формы, соответствующий атрибуту 'category', заполнится значением текущей категории.
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title,
               'update_form': product_form,
               'category': category
               }

    return render(request, 'adminapp/product_update.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Детальная информация'
        context['icon'] = 'bx-chair'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'

    def get_form(self, form_class=ProductEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Править: "{context.get(self, self.object.name)}"'
        context['icon'] = 'bx-edit'
        return context

    def get_success_url(self):
        return reverse_lazy('adminapp:product_read', args=(self.object.id,))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'удалить: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    def get_success_url(self):
        return reverse_lazy('adminapp:products', args=(self.object.category_id,))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

