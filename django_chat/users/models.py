from typing import Iterable, Optional
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for django chat.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_("First Name"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name"), blank=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Patient(models.Model):
    """
    Patient model for django chat.
    """

    PATIENT_ILLNESS = (
        ("Asthma", "Asthma"),
        ("Cancer", "Cancer"),
        ("Diabetes", "Diabetes"),
        ("Heart Disease", "Heart Disease"),
        ("Hypertension", "Hypertension"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    illness = models.CharField(
        _("Illness"), blank=True, max_length=255, choices=PATIENT_ILLNESS
    )

    def get_absolute_url(self):
        """Get url for patient's detail view.

        Returns:
            str: URL for patient detail.

        """
        return reverse("users:patient-detail", kwargs={"username": self.user.username})


class Doctor(models.Model):
    """
    Doctor model for django chat.
    """

    DOCTOR_SPECIALIZATION = (
        ("Cardiologist", "Cardiologist"),
        ("Dentist", "Dentist"),
        ("Dermatologist", "Dermatologist"),
        ("Endocrinologist", "Endocrinologist"),
        ("Gastroenterologist", "Gastroenterologist"),
        ("Neurologist", "Neurologist"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    specialization = models.CharField(
        _("Specialization"), blank=True, max_length=255, choices=DOCTOR_SPECIALIZATION
    )
    patients = models.ManyToManyField(Patient, related_name="doctor", blank=True)

    def get_absolute_url(self):
        """Get url for doctor's detail view.

        Returns:
            str: URL for doctor detail.

        """
        return reverse("users:doctor-detail", kwargs={"username": self.user.username})
