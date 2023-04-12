from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings as jwt_settings


def set_refresh_cookie(response, refresh_token):
    cookie_name = settings.JWT_AUTH_COOKIE
    token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
    response.set_cookie(
        cookie_name,
        value=refresh_token,
        expires=token_expiration,
        httponly=True,
        samesite="None",
        secure=True,
    )


def unset_refresh_cookie(response):
    response.delete_cookie(settings.JWT_AUTH_COOKIE)


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        cookie_name = settings.JWT_AUTH_COOKIE
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(cookie_name)
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
