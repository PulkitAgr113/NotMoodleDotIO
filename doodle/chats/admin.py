from django.contrib import admin
from .models import ChatMessage
from .models import Room

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Room)