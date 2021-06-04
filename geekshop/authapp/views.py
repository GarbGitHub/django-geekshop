from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)  # Все данные из формы полученные методом POST
    if request.method == 'POST' and login_form.is_valid():  # если POST
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)  # авторизован или нет
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    content = {'title': title,
               'login_form': login_form,}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
