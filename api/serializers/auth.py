from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_settings


class CookieTokenObtainSerializer(serializers.Serializer):
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


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def extract_refresh_token(self):
        request = self.context["request"]
        # Override token extraction to allow for refresh token in request body
        if "refresh" in request.data and request.data["refresh"]:
            return request.data["refresh"]
        # Default with refresh token in HttpOnly cookie
        cookie_name = settings.JWT_AUTH_COOKIE
        if cookie_name and cookie_name in request.COOKIES:
            return request.COOKIES[cookie_name]
        else:
            raise InvalidToken("No valid token found")

    def validate(self, attrs):
        # validates and isused to build a new JWT
        refresh = self.token_class(self.extract_refresh_token())

        data = {"access": str(refresh.access_token)}
        if jwt_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
        data["refresh"] = str(refresh)
        return data
