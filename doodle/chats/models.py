from django.db import models
from django.contrib.auth.forms import User

# Create your models here.
class Chat(models.Model):
    room_name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return str(self.room_name)
    
    def get_messages(self):
        return self.messages.all()

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    nick = models.CharField(max_length=120)
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.chat.room_name}-{self.nick}"

class Code(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_username = models.CharField(max_length=100, default="")
    room_code = models.CharField(max_length=6, default="")
    room_type = models.CharField(max_length=7, default="")

    def __str__(self) -> str:
        return self.room_code

