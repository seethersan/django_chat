from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_chat.users.models import Patient, Doctor

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name"]


class DoctorSerializer(serializers.ModelSerializer):
    patients = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.filter(), many=True
    )

    class Meta:
        model = Patient
        fields = ["username", "name", "first_name", "last_name", "specialization"]
        extra_kwargs = {"patients": {"required": False}}


class PatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True, many=True)

    class Meta:
        model = Patient
        fields = ["username", "name", "first_name", "last_name", "illness"]
        extra_kwargs = {"doctors": {"required": False}}
