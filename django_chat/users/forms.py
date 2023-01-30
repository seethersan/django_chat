from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms


from .models import Patient, Doctor

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"] = forms.CharField(max_length=30, label="First Name")
        self.fields["last_name"] = forms.CharField(max_length=30, label="Last Name")
        self.fields["account_type"] = forms.ChoiceField(
            choices=[("patient", "Patient"), ("doctor", "Doctor")], label="Account Type"
        )
        self.fields["illness"] = forms.ChoiceField(
            choices=Patient.PATIENT_ILLNESS, label="Illness"
        )
        self.fields["specialization"] = forms.ChoiceField(
            choices=Doctor.DOCTOR_SPECIALIZATION, label="Specialization"
        )

    def save(self, request):
        account_type = self.cleaned_data.pop("account_type")
        illness = self.cleaned_data.pop("illness")
        specialization = self.cleaned_data.pop("specialization")
        user = super(UserSignupForm, self).save(request)

        if account_type == "patient":
            patient = Patient.objects.create(
                user=user,
                illness=illness,
            )
            patient.save()
        elif account_type == "doctor":
            doctor = Doctor.objects.create(
                user=user,
                specialization=specialization,
            )
            doctor.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
