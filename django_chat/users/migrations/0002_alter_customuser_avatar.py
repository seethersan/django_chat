# Generated by Django 5.0.6 on 2024-05-21 23:51

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                default="avatar/default_avatar_profile.jpg",
                upload_to=users.models.get_path_name,
            ),
        ),
    ]
