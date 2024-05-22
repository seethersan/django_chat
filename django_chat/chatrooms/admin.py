from django.contrib import admin

from .models import ChatRoom


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(ChatRoom, ChatRoomAdmin)
