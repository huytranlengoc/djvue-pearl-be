from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.authentications import set_refresh_cookie, unset_refresh_cookie
from api.serializers import (CookieTokenObtainSerializer,
                             CookieTokenRefreshSerializer)


class CookieTokenObtainView(TokenObtainPairView):
    """
    Same as rest_framework_simplejwt.views.TokenObtainPairView but:
        * set HttpOnly cookie to store refresh token
        * remove `refresh` from response data.
    """

    serializer_class = CookieTokenObtainSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Override from rest_framework_simplejwt.views.TokenRefreshView:
        * set HttpOnly cookie to store refresh token
        * remote `refresh` from response data.
    """

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenLogoutView(APIView):
    def post(self, request):
        response = Response()
        unset_refresh_cookie(response)
        response.data = {
            "detail": _("You have been successfully logged out."),
        }
        return response
