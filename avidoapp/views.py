from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from avidoapp.forms import *


def main_view(request):
    adverts = AdvertModel.objects.all()
    return render(request, 'main.html', {'adverts': adverts})


def create_advert(request, choice):
    match choice:
        case 1:
            form1 = CarForm()
        case 2:
            form1 = HouseForm()
        case 3:
            form1 = JobForm()
    form2 = AdvertForm()
    form3 = ImageForm()
    if request.method == 'POST':
        form1 = CarForm(request.POST)
        form2 = AdvertForm(request.POST)
        form3 = ImageForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            advert_object = form1.save()
            advert = form2.save(commit=False)
            user = get_object_or_404(User, id=request.user.id)
            advert.author = user
            advert.ad_object = advert_object
            advert.save()
            for f in request.FILES.getlist('photos'):
                images = ImageModel(image=f, advert=advert)
                images.save()
            return redirect('main')
    return render(request, 'create_advert.html', {'form1': form1, 'form2': form2, 'form3': form3})


def other_advert(request):
    form2 = AdvertForm()
    form3 = ImageForm()
    if request.method == 'POST':
        form2 = AdvertForm(request.POST)
        form3 = ImageForm(request.POST, request.FILES)
        if form2.is_valid() and form3.is_valid():
            advert = form2.save(commit=False)
            user = get_object_or_404(User, id=request.user.id)
            advert.author = user
            advert.save()
            for f in request.FILES.getlist('photos'):
                images = ImageModel(image=f, advert=advert)
                images.save()
            return redirect('main')
    return render(request, 'create_advert.html', {'form2': form2, 'form3': form3})


def advert_view(request, id):
    advert = get_object_or_404(AdvertModel, id=id)
    images = ImageModel.objects.filter(advert=id)
    return render(request, 'advert_view.html', {'advert': advert, 'images': images})


def chat_view(request, advert_id):
    form = MessageForm()
    advert = get_object_or_404(AdvertModel, id=advert_id)
    if ChatModel.objects.filter(advert=advert).exists():
        chat = ChatModel.objects.get(advert=advert)
        messages = MessageModel.objects.filter(chat=chat)
    else:
        messages = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=request.user.id)
            if not ChatModel.objects.filter(advert=advert).exists():
                chat = ChatModel(advert=advert, customer=user)
                chat.save()
            else:
                chat = ChatModel.objects.get(advert=advert)
            message = form.save(commit=False)
            message.chat = chat
            message.author = user
            message.save()
            return redirect('chat', advert_id)
    return render(request, 'chat.html', {'form': form, 'advert': advert, 'messages': messages})


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
                if user.is_block == True and user.time_unblock > timezone.now():
                    return HttpResponse('Вы заблокированы')
                else:
                    user.is_block = False
                    user.save()
                login(request, user)
                return redirect("main")
    return render(request, 'auth.html', {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect("auth")
