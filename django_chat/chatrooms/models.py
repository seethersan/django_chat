from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="chatrooms")

    def __str__(self):
        return self.name
