import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom
from django_chat.chat_storage import AsyncChatStorage

# Initialize the logger
logger = logging.getLogger("chatrooms.consumers")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        logger.info(f"User {self.scope['user']} connecting to room {self.room_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info(f"User {self.scope['user']} connected to room {self.room_name}")

    async def disconnect(self, close_code):
        logger.info(
            f"User {self.scope['user']} disconnecting from room {self.room_name} with code {close_code}"
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(
            f"User {self.scope['user']} disconnected from room {self.room_name}"
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.user = self.scope["user"]

        logger.debug(
            f"Message received from user {self.user.id} in room {self.room_name}: {message}"
        )

        storage = AsyncChatStorage()

        room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        chats = await storage.get_chat(room.name, [])
        chats.append(
            {
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "avatar": self.user.avatar.url if self.user.avatar else None,
                },
                "content": message,
                "room": room.name,
            }
        )
        await storage.set_chat(room.name, chats)

        logger.debug(f"Message stored for room {self.room_name} by user {self.user.id}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "avatar": self.user.avatar.url if self.user.avatar else None,
                },
            },
        )

        logger.debug(
            f"Message sent to group {self.room_group_name} from user {self.user.id}"
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        logger.debug(
            f"Broadcasting message in room {self.room_name} from user {user['id']}: {message}"
        )

        await self.send(text_data=json.dumps({"message": message, "user": user}))

        logger.debug(
            f"Message broadcasted in room {self.room_name} from user {user['id']}: {message}"
        )
