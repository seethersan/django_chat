from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_chat.users.models import Patient, Doctor

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "password"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patients = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.filter(), many=True
    )

    class Meta:
        model = Doctor
        fields = [
            "user",
            "specialization",
            "patients",
        ]

    def create(self, validated_data):
        data = validated_data.pop("user")
        user = User.objects.create_user(**data)
        validated_data.update({"user": user})
        return super().create(validated_data)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    doctors = DoctorSerializer(read_only=True, many=True)

    class Meta:
        model = Patient
        fields = ["user", "illness", "doctors"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        data = validated_data.pop("user")
        user = User.objects.create_user(**data)
        validated_data.update({"user": user})
        return super().create(validated_data)
