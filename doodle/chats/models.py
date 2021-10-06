from django.db import models

# Create your models here.
class Chat(models.Model):
    room_name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return str(self.room_name)
    
    def get_messages(self):
        return self.messages.all()