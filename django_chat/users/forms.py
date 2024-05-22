from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.images import get_image_dimensions
from django import forms


class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "avatar")

    def signup(self, request, user):
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.avatar = self.cleaned_data.get("avatar")
        user.save()

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 2500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    "Please use an image that is "
                    "%s x %s pixels or smaller." % (max_width, max_height)
                )

            # validate content type
            main, sub = avatar.content_type.split("/")
            if not (main == "image" and sub in ["jpeg", "pjpeg", "gif", "png"]):
                raise forms.ValidationError("Please use a JPEG, " "GIF or PNG image.")

            # validate file size
            if len(avatar) > (2048 * 1024):
                raise forms.ValidationError("Avatar file size may not exceed 2MB.")

        except TypeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "avatar")

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 2500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    "Please use an image that is "
                    "%s x %s pixels or smaller." % (max_width, max_height)
                )

            # validate content type
            main, sub = avatar.content_type.split("/")
            if not (main == "image" and sub in ["jpeg", "pjpeg", "gif", "png"]):
                raise forms.ValidationError("Please use a JPEG, " "GIF or PNG image.")

            # validate file size
            if len(avatar) > (2048 * 1024):
                raise forms.ValidationError("Avatar file size may not exceed 20k.")

        except TypeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
