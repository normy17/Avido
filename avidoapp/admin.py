from django.contrib import admin

from avidoapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(AdvertModel)
admin.site.register(ImageModel)
admin.site.register(AdObjectModel)
admin.site.register(ChatModel)
admin.site.register(MessageModel)