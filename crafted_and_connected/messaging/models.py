# messaging/models.py
from django.db import models
from crafted_and_connected.authentication.models import CustomUser
from django.utils import timezone


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
