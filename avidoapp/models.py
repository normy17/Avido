from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images', verbose_name='Аватар', blank=True, null=True)
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    rating = models.FloatField(verbose_name='Рейтинг', default=0)
    is_block = models.BooleanField(verbose_name='Блокировка', default=False)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class AdObjectModel(models.Model):
    car_make = models.CharField(max_length=256, verbose_name='Марка машины', null=True)
    car_model = models.CharField(max_length=256, verbose_name='Модель машины', null=True, blank=True)
    year_of_issue = models.IntegerField(verbose_name='Год выпуска', validators=[
        MaxValueValidator(2024),
        MinValueValidator(1950)
    ], default=2000, null=True, blank=True)
    color = models.CharField(max_length=256, verbose_name='Цвет', null=True, blank=True)
    body_type = models.CharField(max_length=256, verbose_name='Вид кузова', choices=(
        ('Седан', 'Седан'),
        ('Хэтчбек', 'Хэтчбек'),
        ('Пикап', 'Пикап'),
        ('Лимузин', 'Лимузин'),
        ('Универсал', 'Универсал'),
        ('Минивэн', 'Минивэн'),
        ('Купе', 'Купе'),
        ('Кабриолет', 'Кабриолет')
    ), null=True, blank=True)
    fuel_type = models.CharField(max_length=256, verbose_name='Вид топлива', choices=(
        ('Бензин', 'Бензин'),
        ('Дизель', 'Дизель'),
        ('Пропан', 'Пропан'),
        ('Электричество', 'Электричество')
    ), null=True, blank=True)
    mileage = models.IntegerField(verbose_name='Пробег', null=True, blank=True)
    property_type = models.CharField(max_length=256, verbose_name='Тип недвижимости', choices=(
        ('Квартира', 'Квартира'),
        ('Дом', 'Дом'),
        ('Прочее', 'Прочее')
    ), null=True)
    area = models.IntegerField(verbose_name='Площадь', null=True, blank=True)
    rooms = models.IntegerField(verbose_name='Количество комнат', null=True, blank=True)
    floors = models.IntegerField(verbose_name='Этаж/этажность', null=True, blank=True)
    state = models.CharField(max_length=256, verbose_name='Состояние', choices=(
        ('Первичное жилье', 'Первичное жилье'),
        ('Вторичное жилье', 'Вторичное жилье')
    ), null=True, blank=True)
    job_title = models.CharField(max_length=256, null=True, verbose_name='Название вакансии')
    requirements = models.TextField(null=True, blank=True, verbose_name='Требования')
    responsibilities = models.TextField(null=True, blank=True, verbose_name='Обязанности')
    schedule = models.TextField(null=True, blank=True, verbose_name='График работы')

    class Meta:
        verbose_name = 'Объект продажи'
        verbose_name_plural = 'Объекты продаж'


class AdvertModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ad_object = models.ForeignKey(AdObjectModel, on_delete=models.CASCADE, verbose_name='Объект продажи', null=True)
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    is_displayed = models.BooleanField(default=True, verbose_name='Отображать?')

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
    creation_time = models.DateTimeField(default=timezone.now, verbose_name='Дата создания сообщения')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='Фотография', blank=True)
    advert = models.ForeignKey(AdvertModel, on_delete=models.CASCADE, verbose_name='Объявление')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'