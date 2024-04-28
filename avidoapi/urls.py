from django.urls import path

from avidoapi.views import block_user

urlpatterns = [
    path('user/block/<int:id>/', block_user, name='block_user')
]