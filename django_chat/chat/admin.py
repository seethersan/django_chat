from django.contrib import admin
from django_chat.chat.models import Conversation, Message


admin.site.register(Conversation)
admin.site.register(Message)
