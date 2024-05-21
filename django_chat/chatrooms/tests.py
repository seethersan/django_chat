from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import ChatRoom

User = get_user_model()


class ChatRoomModelTest(TestCase):
    def setUp(self):
        self.room_name = "Test Room"
        self.chat_room = ChatRoom.objects.create(name=self.room_name)

    def test_create_chat_room(self):
        room = ChatRoom.objects.create(name="New Test Room")
        self.assertEqual(room.name, "New Test Room")
        self.assertTrue(isinstance(room, ChatRoom))


class ChatRoomViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.chatroom = ChatRoom.objects.create(name="Test Room")

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatrooms/list_rooms.html")
        self.assertContains(response, "Test Room")

    def test_create_room_view_get(self):
        response = self.client.get(reverse("create_room"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatrooms/index.html")


class RoomViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_name = "test-room"
        self.chat_room = ChatRoom.objects.create(name=self.room_name)
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    @patch("django_chat.chat_storage.ChatStorage.get_chat")
    def test_room_view_existing_chat_room(self, mock_get_chat):
        mock_get_chat.return_value = []

        url = reverse("room", args=[self.room_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatrooms/room.html")
        self.assertContains(response, self.room_name)
        self.assertIn("chats", response.context)

        mock_get_chat.assert_called_once_with(self.room_name, [])

    @patch("django_chat.chat_storage.ChatStorage.get_chat")
    def test_room_view_existing_chat_room_with_chats(self, mock_get_chat):
        mock_get_chat.return_value = [
            {"user": 1, "content": "test message", "room": "test-room"},
            {"user": 2, "content": "another test message", "room": "test-room"},
        ]

        url = reverse("room", args=[self.room_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatrooms/room.html")
        self.assertContains(response, self.room_name)
        self.assertIn("chats", response.context)
        self.assertEqual(len(response.context["chats"]), 2)

        mock_get_chat.assert_called_once_with(self.room_name, [])

    def test_room_view_non_existing_chat_room(self):
        new_room_name = "new-test-room"
        url = reverse("room", args=[new_room_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatrooms/room.html")
        self.assertContains(response, new_room_name)
        self.assertIn("chats", response.context)

        # Verify that the new chat room is created
        new_chat_room = ChatRoom.objects.get(name=new_room_name)
        self.assertIsNotNone(new_chat_room)
