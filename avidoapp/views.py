from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from avidoapp.forms import *


def main_view(request):
    return render(request, 'main.html')


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )

            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "registration.html", {
        "form": form,
        "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Неправильный логин или пароль")
            else:
                # if user.profile.is_blocked == True and user.profile.time_unblock > timezone.now():
                #     return HttpResponse('Вы заблокированы')
                # else:
                #     user.profile.is_blocked = False
                #     user.profile.save()
                login(request, user)
                return redirect("main")
    return render(request, 'auth.html', {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect("auth")