from django.db import models
from django.contrib.auth.forms import User

# Create your models here.

class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room_code = models.CharField(max_length=6, default="")
    room_type = models.CharField(max_length=7, default="")
    canvas_data_url = models.TextField(default="none")
    started = models.BooleanField(default=False)
    done_players = models.ManyToManyField(User, related_name="done_players")
    rem_players = models.ManyToManyField(User, related_name="rem_players")
    current_player = models.ForeignKey(User, on_delete=models.SET(owner), related_name="current_player")
    guessed = models.ManyToManyField(User, related_name="guessed")
    word = models.CharField(max_length=100, default="")
    startTime = models.DateTimeField(auto_now_add=True)
    round_no = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.room_code

class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(default="")
    author = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.room.room_code}-{self.text}"

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_score")
    score = models.IntegerField(default=0)
    high_score = models.IntegerField(default=0)
