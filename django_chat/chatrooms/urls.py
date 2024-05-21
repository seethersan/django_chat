from django.urls import path
from .views import Index, RoomCreate, Room

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("create/", RoomCreate.as_view(), name="create_room"),
    path("<str:room_name>/", Room.as_view(), name="room"),
]
