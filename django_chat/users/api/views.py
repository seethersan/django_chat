from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


from .serializers import (
    UserSerializer,
    DoctorSerializer,
    PatientSerializer,
)
from ..models import Doctor, Patient

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def all(self, request):
        serializer = UserSerializer(
            User.objects.all(), many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def doctor_patient(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            patient = None
        if patient:
            doctors = Doctor.objects.filter(patients=patient)
            serializer = DoctorSerializer(
                doctors, many=True, context={"request": request}
            )
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            doctor = None
        if doctor:
            patients = Patient.objects.filter(doctor=doctor)
            serializer = PatientSerializer(
                patients, many=True, context={"request": request}
            )

        return Response(
            status=status.HTTP_200_OK,
            data=[
                {"username": data["user"]["username"], "name": data["user"]["name"]}
                for data in serializer.data
            ],
        )


class CustomObtainAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class DoctorViewSet(viewsets.ModelViewSet):
    """
    List all doctors, or create a new doctor.
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    ordering_fields = ["name"]


class PatientViewSet(viewsets.ModelViewSet):
    """
    List all patient, or create a new patient.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]
