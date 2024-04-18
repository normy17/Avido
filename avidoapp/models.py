from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    rating = models.FloatField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class AdObjectModel(models.Model):
    car_make = models.CharField(max_length=256, verbose_name='Марка машины', null=True, blank=True)
    car_model = models.CharField(max_length=256, verbose_name='Модель машины', null=True, blank=True)
    year_of_issue = models.IntegerField(verbose_name='Год выпуска', validators=[
        MaxValueValidator(2024),
        MinValueValidator(1950)
    ], default=2000, null=True, blank=True)
    color = models.CharField(max_length=256, verbose_name='Цвет', null=True, blank=True)
    body_type = models.CharField(max_length=256, verbose_name='Вид кузова', choices=(
        ('Sedan', 'Седан'),
        ('Hatchback', 'Хэтчбек'),
        ('Pickup', 'Пикап'),
        ('Limousine', 'Лимузин'),
        ('Universal', 'Универсал'),
        ('Minivan', 'Минивэн'),
        ('Coupe', 'Купе'),
        ('Cabriolet', 'Кабриолет')
    ), null=True, blank=True)
    fuel_type = models.CharField(max_length=256, verbose_name='Вид топлива', choices=(
        ('Petrol', 'Бензин'),
        ('Diesel', 'Дизель'),
        ('Propane', 'Пропан'),
        ('Electricity', 'Электричество')
    ), null=True, blank=True)
    mileage = models.IntegerField(verbose_name='Пробег', null=True, blank=True)
    property_type = models.CharField(max_length=256, verbose_name='Тип недвижимости', choices=(
        ('Apartment', 'Квартира'),
        ('House', 'Дом'),
        ('Other', 'Прочее')
    ), null=True, blank=True)
    area = models.IntegerField(verbose_name='Площадь', null=True, blank=True)
    rooms = models.IntegerField(verbose_name='Количество комнат', null=True, blank=True)
    floors = models.IntegerField(verbose_name='Этаж/этажность', null=True, blank=True)
    state = models.CharField(max_length=256, verbose_name='Состояние', choices=(
        ('Primary housing', 'Первичное жилье'),
        ('Secondary housing', 'Вторичное жилье')
    ), null=True, blank=True)
    job_title = models.CharField(max_length=256, null=True, blank=True, verbose_name='Название вакансии')
    requirements = models.CharField(max_length=256, null=True, blank=True, verbose_name='Требования')
    conditions = models.CharField(max_length=256, null=True, blank=True, verbose_name='Условия работы')
    schedule = models.CharField(max_length=256, null=True, blank=True, verbose_name='График работы')
    contacts = models.CharField(max_length=256, null=True, blank=True,
                                verbose_name='Контактная информация работодателя')

    class Meta:
        verbose_name = 'Объект продажи'
        verbose_name_plural = 'Объекты продаж'


class AdvertModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ad_object = models.ForeignKey(AdObjectModel, on_delete=models.CASCADE, verbose_name='Объект продажи')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    is_displayed = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ChatModel(models.Model):
    advert = models.ForeignKey(AdvertModel, on_delete=models.CASCADE, verbose_name='Объявление')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class MessageModel(models.Model):
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE, verbose_name='Чат')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор сообщения')
    creation_time = models.DateTimeField(verbose_name='Дата создания сообщения')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class ImageModel(models.Model):
    images = models.ImageField(upload_to='images', verbose_name='Фотография')
    advert = models.ForeignKey(AdvertModel, on_delete=models.CASCADE, verbose_name='Объявление')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
