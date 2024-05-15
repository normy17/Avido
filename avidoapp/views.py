from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Max
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta

from avidoapp.forms import *


def main_view(request):
    adverts = AdvertModel.objects.filter(is_displayed=True).order_by('-publication_date')
    all_adverts = True
    query = request.GET.get('q')
    if query:
        adverts = AdvertModel.objects.filter(Q(title__iregex=query), is_displayed=True).order_by('-publication_date')
    return render(request, 'main.html', {'adverts': adverts, 'all_adverts': all_adverts, 'query': query})


def cars_view(request):
    adverts = AdvertModel.objects.filter(ad_object__car_make__isnull=False, is_displayed=True).order_by('-publication_date')
    cars = True
    return render(request, 'main.html', {'adverts': adverts, 'cars': cars})


def houses_view(request):
    adverts = AdvertModel.objects.filter(ad_object__property_type__isnull=False, is_displayed=True).order_by('-publication_date')
    houses = True
    return render(request, 'main.html', {'adverts': adverts, 'houses': houses})


def jobs_view(request):
    adverts = AdvertModel.objects.filter(ad_object__job_title__isnull=False, is_displayed=True).order_by('-publication_date')
    jobs = True
    return render(request, 'main.html', {'adverts': adverts, 'jobs': jobs})


def others_view(request):
    adverts = AdvertModel.objects.filter(ad_object__car_make__isnull=True,
                                         ad_object__property_type__isnull=True,
                                         ad_object__job_title__isnull=True,
                                         is_displayed=True).order_by('-publication_date')
    others = True
    return render(request, 'main.html', {'adverts': adverts, 'others': others})


def my_profile_view(request):
    my_adverts = AdvertModel.objects.filter(author=request.user)
    return render(request, 'my_profile.html', {'my_adverts': my_adverts})


def my_chats_view(request):
    my_chats = ChatModel.objects.filter(advert__author=request.user) | ChatModel.objects.filter(customer=request.user)
    sorted_chats = my_chats.annotate(last_message_time=Max('messagemodel__creation_time')).order_by('-last_message_time')
    return render(request, 'my_chats.html', {'my_chats': sorted_chats})


def choice_advert_view(request):
    return render(request, 'choice_advert.html')


def create_advert_view(request, choice):
    form = None
    match choice:
        case 1:
            form = CarForm
        case 2:
            form = HouseForm
        case 3:
            form = JobForm
    form2 = AdvertForm()
    form3 = ImageForm()
    if request.method == 'POST':
        form1 = form(request.POST)
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
    return render(request, 'create_advert.html', {'form1': form(), 'form2': form2, 'form3': form3})


def other_advert_view(request):
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


def edit_advert_view(request, id):
    is_edit = True
    advert = AdvertModel.objects.get(id=id)
    images = ImageModel.objects.filter(advert=advert)
    form = None
    if advert.ad_object is None:
        form = None
    elif advert.ad_object.car_make:
        form = CarForm
    elif advert.ad_object.property_type:
        form = HouseForm
    elif advert.ad_object.job_title:
        form = JobForm
    form1 = form(instance=advert.ad_object) if advert.ad_object else None
    form2 = AdvertForm(instance=advert)
    form3 = ImageForm()
    if request.method == "POST":
        if form:
            form = form(request.POST, instance=advert.ad_object)
        form2 = AdvertForm(request.POST, instance=advert)
        form3 = ImageForm(request.POST, request.FILES)
        if form and form.is_valid():
            form.save()
        if form2.is_valid():
            form2.save()
            advert.publication_date = timezone.now()
            advert.save()
            for f in request.FILES.getlist('photos'):
                images = ImageModel(image=f, advert=advert)
                images.save()
            return redirect('advert_view', id, 0)
    return render(request, "create_advert.html", {
        "form1": form1,
        'form2': form2,
        'form3': form3,
        'images': images,
        'is_edit': is_edit
    })


def delete_advert_view(request, id):
    advert = AdvertModel.objects.get(id=id)
    advert.delete()
    return redirect('my_profile')


def advert_view(request, id, image=0):
    advert = get_object_or_404(AdvertModel, id=id)
    images = ImageModel.objects.filter(advert=id)
    main_image = images[image] if images else None
    return render(request, 'advert_view.html', {
        'advert': advert,
        'images': images,
        'main_image': main_image
    })


def delete_image_view(request, id):
    image = ImageModel.objects.get(id=id)
    advert = image.advert
    image.delete()
    return redirect('edit_advert', advert.id)


def customer_chat_view(request, advert_id):
    form = MessageForm()
    advert = get_object_or_404(AdvertModel, id=advert_id)
    user = get_object_or_404(User, id=request.user.id)
    if ChatModel.objects.filter(advert=advert, customer=user).exists():
        chat = ChatModel.objects.get(advert=advert, customer=user)
        messages = MessageModel.objects.filter(chat=chat)
        messages_by_date = {}
        for message in messages:
            original_date = message.creation_time
            time_difference = timedelta(hours=3)
            new_date = original_date + time_difference
            date = new_date.date()
            if date not in messages_by_date:
                messages_by_date[date] = []
            messages_by_date[date].append(message)
    else:
        messages_by_date = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            if not ChatModel.objects.filter(advert=advert, customer=user).exists():
                chat = ChatModel(advert=advert, customer=user)
                chat.save()
            else:
                chat = ChatModel.objects.get(advert=advert, customer=user)
            message = form.save(commit=False)
            message.chat = chat
            message.author = user
            message.save()
            return redirect('customer_chat', advert_id)
    return render(request, 'chat.html', {
        'form': form,
        'advert': advert,
        'messages_by_date': messages_by_date
    })


def author_chat_view(request, id):
    chat = ChatModel.objects.get(id=id)
    advert = chat.advert
    messages = MessageModel.objects.filter(chat=chat)
    messages_by_date = {}
    for message in messages:
        original_date = message.creation_time
        time_difference = timedelta(hours=3)
        new_date = original_date + time_difference
        date = new_date.date()
        if date not in messages_by_date:
            messages_by_date[date] = []
        messages_by_date[date].append(message)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = advert.author
            message.save()
            return redirect('author_chat', id)
    return render(request, 'chat.html', {
        'form': form,
        'advert': advert,
        'chat': chat,
        'messages_by_date': messages_by_date
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            else:
                user.avatar = 'images/default-avatar.jpg'
            user.save()
            is_success = True
    return render(request, "registration.html", {
        "form": form,
        "is_success": is_success
    })


def edit_profile_view(request):
    form = EditProfileForm(instance=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    return render(request, "edit_profile.html", {"form": form})


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Неправильный логин или пароль")
            else:
                login(request, user)
                return redirect("main")
    return render(request, 'auth.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect("auth")
