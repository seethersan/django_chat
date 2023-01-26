from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_chat.users.api.views import UserViewSet
from django_chat.chat.api.views import ConversationViewSet, MessageViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)


app_name = "api"
urlpatterns = router.urls
