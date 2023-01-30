import json
from django_chat.users.models import Doctor, Patient
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_chat.chat.models import Message, Conversation
from django_chat.users.api.serializers import (
    DoctorSerializer,
    PatientSerializer,
    UserSerializer,
)


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "content",
            "timestamp",
            "read",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return UserSerializer(obj.to_user).data


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "other_user", "last_message")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        usernames = obj.name.split("__")
        context = {}
        for username in usernames:
            if username != self.context["user"].username:
                # This is the other participant
                other_user = User.objects.get(username=username)
                try:
                    doctor = Doctor.objects.get(user=other_user)
                except Doctor.DoesNotExist:
                    doctor = None
                else:
                    doctor = DoctorSerializer(doctor, context=context).data
                    return {
                        "specialization": doctor["specialization"],
                        "username": doctor["user"]["username"],
                        "name": doctor["user"]["name"],
                        "password": doctor["user"]["password"],
                        "type": "doctor",
                    }

                try:
                    patient = Patient.objects.get(user=other_user)
                except Patient.DoesNotExist:
                    patient = None
                else:
                    patient = PatientSerializer(patient, context=context).data
                    return {
                        "illness": patient["illness"],
                        "username": patient["user"]["username"],
                        "name": patient["user"]["name"],
                        "password": patient["user"]["password"],
                        "type": "patient",
                    }

                return UserSerializer(other_user, context=context).data
