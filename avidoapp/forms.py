from django import forms
from multiupload.fields import MultiFileField
from .models import *


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2', 'phone')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CarForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('car_make', 'car_model', 'year_of_issue', 'color', 'body_type', 'fuel_type', 'mileage')


class HouseForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('property_type', 'area', 'rooms', 'floors', 'state')


class JobForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('job_title', 'requirements', 'conditions', 'schedule', 'contacts')


class AdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertModel
        fields = ('title', 'description', 'price', 'address')


class ImageForm(forms.Form):
    photos = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, label='Фотографии', required=False)


class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = ('text', )