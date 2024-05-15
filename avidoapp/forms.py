from django import forms
from multiupload.fields import MultiFileField
from .models import *


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'avatar', 'password', 'password2')
        labels = {
            'email': '',
            'username': '',
            'first_name': '',
            'last_name': '',
            'phone': '',
            'password': ''
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        }
        help_texts = {
            'username': ''
        }


class AuthForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'avatar')
        labels = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'phone': '',
            'avatar': ''
        }
        widgets = {
            'avatar': forms.FileInput(),
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
        }
        help_texts = {
            'username': ''
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('car_make', 'car_model', 'year_of_issue', 'color', 'body_type', 'fuel_type', 'mileage')
        labels = {'mileage': 'Пробег, км'}


class HouseForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('property_type', 'area', 'rooms', 'floors', 'state')
        labels = {'area': 'Площадь, м²'}


class JobForm(forms.ModelForm):
    class Meta:
        model = AdObjectModel
        fields = ('job_title', 'requirements', 'responsibilities', 'schedule')


class AdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertModel
        fields = ('title', 'description', 'price', 'address', 'is_displayed')
        labels = {'is_displayed': 'Показывать всем'}


class ImageForm(forms.Form):
    photos = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, label='Фотографии', required=False)


class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = ('text', )
        labels = {
            'text': ''
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Написать сообщение'}),
        }