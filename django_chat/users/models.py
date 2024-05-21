from django.db import models
from django.contrib.auth.models import AbstractUser


def get_path_name(instance, filename):
    return f"avatar/{instance.username}_{filename}"


# custom User model
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=get_path_name, blank=True, null=True)
