from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_path_name(instance, filename):
    return f"avatar/{uuid4()}_{filename}"


# custom User model
class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to=get_path_name, default="avatar/default_avatar_profile.jpg"
    )
