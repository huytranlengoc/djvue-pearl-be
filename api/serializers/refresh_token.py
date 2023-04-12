from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_settings


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
