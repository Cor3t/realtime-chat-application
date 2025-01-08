from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    ROOM_TYPE_CHOICES = (
        ('private', 'PRIVATE'),
        ('group', 'GROUP')
    )

    name = models.CharField(max_length=255, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    paticipants = models.ManyToManyField(User, related_name='chatrooms')


    def __str__(self):
        return self.name
    

class Messages(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"