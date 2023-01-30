from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django_chat.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

from django_chat.users.api.views import DoctorViewSet, PatientViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="doctor")
router.register(r"doctors", DoctorViewSet, basename="patient")


app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path(r"", include(router.urls)),
]
