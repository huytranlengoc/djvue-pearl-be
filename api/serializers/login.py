from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(email=email, password=password)
            # check valid credentials
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise exceptions.ValidationError(msg)
            # check user status
            if not user.is_active:
                msg = _("User account is disabled.")
                raise exceptions.ValidationError(msg)
            # valid user
            data["user"] = user
        else:
            msg = _("Must include 'email' and 'password'.")
            raise exceptions.ValidationError(msg)
        return data
