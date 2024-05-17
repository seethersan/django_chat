from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from unittest.mock import patch

from chatrooms.consumers import ChatConsumer
from chatrooms.models import ChatRoom

test_settings = override_settings(
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    },
)


@test_settings
class ChatConsumerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.room_name = "test-room"
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_room = ChatRoom.objects.create(name=self.room_name)

    async def test_connect_and_disconnect(self):
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/chat/{self.room_name}/"
        )
        communicator.scope["user"] = self.user
        communicator.scope["url_route"] = {"kwargs": {"room_name": self.room_name}}
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()

    @patch("django_chat.chat_storage.AsyncChatStorage.set_chat")
    @patch("django_chat.chat_storage.AsyncChatStorage.get_chat")
    async def test_receive_message(self, mock_get_chat, mock_set_chat):
        message = "hello"

        mock_get_chat.return_value = []
        mock_set_chat.return_value = [
            {"user": self.user.id, "content": message, "room": self.room_name}
        ]

        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/chat/{self.room_name}/"
        )
        communicator.scope["user"] = self.user
        communicator.scope["url_route"] = {"kwargs": {"room_name": self.room_name}}
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({"message": message})

        response = await communicator.receive_json_from()
        self.assertEqual(response, {"message": message, "user_id": self.user.id})

        mock_get_chat.assert_called_once_with(self.room_name, [])
        mock_set_chat.assert_called_once_with(
            self.room_name,
            [{"user": self.user.id, "content": message, "room": self.room_name}],
        )

        await communicator.disconnect()
