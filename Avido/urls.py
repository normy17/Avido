from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('avidoapp.urls')),
    path('api/', include('avidoapi.urls'))
]
