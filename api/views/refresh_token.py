from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView

from api.authentications import set_refresh_cookie
from api.serializers import CookieTokenRefreshSerializer


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            set_refresh_cookie(response, response.data["refresh"])
            del response.data["refresh"]

        return super().finalize_response(request, response, *args, **kwargs)
