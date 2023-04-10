from django.conf import settings
from rest_framework import serializers, status
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE,
        value=refresh_token,
        httponly=True,
        max_age=settings.JWT_AUTH_COOKIE_MAX_AGE,
        samesite="None",
        secure=True,
    )


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
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()
        data["refresh"] = str(refresh)
        return data


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]

        return super().finalize_response(request, response, *args, **kwargs)
