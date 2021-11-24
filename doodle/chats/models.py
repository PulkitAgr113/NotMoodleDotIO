from django.db import models
from django.contrib.auth.forms import User

# Create your models here.

class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_username = models.CharField(max_length=100, default="")
    room_code = models.CharField(max_length=6, default="")
    room_type = models.CharField(max_length=7, default="")
    canvas_data_url = models.TextField(default="none")

    def __str__(self) -> str:
        return self.room_code

class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(default="")
    author = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.room.room_code}-{self.text}"


