from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ChatRoom
from django_chat.chat_storage import ChatStorage

class Index(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'chatrooms/index.html')

class Room(LoginRequiredMixin, View):
	def get(self, request, room_name):
		room = ChatRoom.objects.filter(name=room_name).first()
		chats = []

		storage = ChatStorage()

		if room:
			chats = storage.get_chat(room_name, [])
		else:
			room = ChatRoom(name=room_name)
			room.save()

		return render(request, 'chatrooms/room.html', {'room_name': room_name, 'chats': chats})