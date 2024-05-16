from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('choice_advert/', choice_advert_view, name='choice_advert'),
    path('create_advert/<int:choice>/', create_advert_view, name='create_advert'),
    path('create_advert/', other_advert_view, name='other_advert'),
    path('advert/<int:id>/', advert_view, name='advert_view'),
    path('edit_advert/<int:id>/', edit_advert_view, name='edit_advert'),
    path('delete_advert/<int:id>/', delete_advert_view, name='delete_advert'),
    path('delete_image/<int:id>/', delete_image_view, name='delete_image'),
    path('customer_chat/<int:advert_id>/', customer_chat_view, name='customer_chat'),
    path('author_chat/<int:id>/', author_chat_view, name='author_chat'),
    path('cars/', cars_view, name='cars'),
    path('houses/', houses_view, name='houses'),
    path('jobs/', jobs_view, name='jobs'),
    path('others/', others_view, name='others'),
    path('my_profile/', my_profile_view, name='my_profile'),
    path('my_chats/', my_chats_view, name='my_chats'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)