from django.contrib import admin
from .models import ChatMessage, Room, Score

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Room)
admin.site.register(Score)
