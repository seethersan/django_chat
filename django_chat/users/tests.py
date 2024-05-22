from django import forms
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from users.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class UserModelTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@email.com",
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password("testpassword"))

    def test_avatar_upload_path(self):
        user = User.objects.create_user(
            email="test@email.com",
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        avatar = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x00\x01\x02\x03",
            content_type="image/jpeg",
        )
        user.avatar = avatar
        user.save()
        self.assertRegex(user.avatar.name, r"avatar\/[a-z0-9-]+_test_image.jpg")

    def test_default_avatar(self):
        user = User.objects.create_user(
            email="test@email.com",
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.avatar.name, "avatar/default_avatar_profile.jpg")
