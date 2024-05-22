import logging
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ChatRoom
from django_chat.chat_storage import ChatStorage

# Initialize the logger
logger = logging.getLogger("chatrooms.views")


class Index(LoginRequiredMixin, View):
    def get(self, request):
        rooms = ChatRoom.objects.all()
        logger.debug(f"Index view accessed by user: {request.user}")
        return render(request, "chatrooms/list_rooms.html", {"rooms": rooms})


class RoomCreate(LoginRequiredMixin, View):
    def get(self, request):
        logger.debug(f"RoomCreate view accessed by user: {request.user}")
        return render(request, "chatrooms/index.html")


class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        logger.debug(
            f"Room view accessed by user: {request.user}, room_name: {room_name}"
        )

        room = ChatRoom.objects.filter(name=room_name).first()
        if room:
            logger.info(f"Existing room found: {room_name}")
            storage = ChatStorage()
            chats = storage.get_chat(room_name, [])
            if request.user not in room.users.all():
                room.users.add(request.user)
                room.save()
            logger.debug(f"Chats retrieved for room: {room_name}, chats: {chats}")
        else:
            logger.info(f"Creating new room: {room_name}")
            room = ChatRoom(name=room_name)
            room.save()
            room.users.add(request.user)
            room.save()
            chats = []

        response = render(
            request, "chatrooms/room.html", {"room_name": room_name, "chats": chats}
        )
        logger.debug(f"Room view response prepared for room_name: {room_name}")
        return response
