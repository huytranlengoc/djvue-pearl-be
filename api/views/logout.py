from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

from api.authentications import unset_refresh_cookie


class LogoutApiView(APIView):
    def post(self, request):
        response = Response()
        unset_refresh_cookie(response)
        response.data = {
            "detail": _("You have been successfully logged out."),
        }
        return response
