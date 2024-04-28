from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('create_advert/<int:choice>/', create_advert, name='create_advert'),
    path('create_advert/', other_advert, name='other_advert'),
    path('advert/<int:id>/', advert_view, name='advert_view'),
    path('chat/<int:advert_id>/', chat_view, name='chat')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)