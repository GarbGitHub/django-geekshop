from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, DivErrorList
from django.contrib import auth
from django.urls import reverse, reverse_lazy

from authapp.models import ShopUser


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None,
                                   error_class=DivErrorList)  # Все данные из формы полученные методом POST

    next = request.GET['next'] if 'next' in request.GET.keys() else ''  # next=/basket/add/3/

    if request.method == 'POST' and login_form.is_valid():  # если POST
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)  # авторизован или нет
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {'title': title,
               'login_form': login_form,
               'next': next,
               }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'
    context = {
        'title': title,
    }

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES, error_class=DivErrorList)

        if register_form.is_valid():
            email = request.POST['email']
            user = register_form.save()

            if send_verify_mail(user):
                print('сообщение отправлено')
                context['message'] = f'Проверьте почту {email} для завершения регистрации'
                register_form = None
                # return HttpResponseRedirect(reverse('auth:login'))

            else:
                print('сообщение НЕ отправлено')
                context['message'] = 'Произошла не предвиденная ошибка'
                # return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context['register_form'] = register_form

    return render(request, 'authapp/register.html', context)


class UserEditView(UpdateView):
    model = ShopUser
    template_name = 'authapp/edit.html'
    context_object_name = 'edit_user'

    def get_form(self, form_class=ShopUserEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('auth:edit', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f'пользователь: {context.get(self, self.object.username)}'
        context['title'] = title
        context['icon'] = 'bx-edit'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {'title': title,
               'edit_form': edit_form}

    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username}, на сайте {settings.DOMAIN_NAME} - пройдите по ссылке: ' \
              f'<a href="{settings.DOMAIN_NAME}{verify_link}"> Активировать </a>'

    # при значении fail_silently = False, в случае неудачной отправки, генерируется ошибка smtplib.SMTPException)
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        context = {'title': 'Верификация'}
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html', context)
        else:
            print(f'activation key error in user: {user.username}')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'Error activation user: {err.args}')
        return HttpResponseRedirect(reverse('index'))
