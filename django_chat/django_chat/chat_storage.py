import json

from redis import StrictRedis
import redis.asyncio as async_redis

from django.conf import settings

CHAT_KEY = "chat"


class ChatStorage:
    def __init__(self):
        self.redis = StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

    def get_chat(self, room_name, default=None):
        chats = self.redis.hget(room_name, CHAT_KEY)
        return json.loads(chats) if chats else default

    def set_chat(self, room_name, chat):
        return self.redis.hset(room_name, mapping={CHAT_KEY: json.dumps(chat)})


class AsyncChatStorage:
    def __init__(self):
        self.pool = async_redis.ConnectionPool.from_url(
            f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
        )

    async def get_chat(self, room_name, default=None):
        async with async_redis.Redis(connection_pool=self.pool) as redis:
            chats = await redis.hget(room_name, CHAT_KEY)
            return json.loads(chats) if chats else default

    async def set_chat(self, room_name, chat):
        async with async_redis.Redis(connection_pool=self.pool) as redis:
            return await redis.hset(room_name, mapping={CHAT_KEY: json.dumps(chat)})
