from django.contrib import admin
from .models import Chat
from .models import ChatMessage
from .models import Code

# Register your models here.
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Code)