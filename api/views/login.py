from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.authentications import set_refresh_cookie
from api.serializers import LoginSerializer


class LoginApiView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data

        # validate credentials
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # get user and generate token
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        # set cookie and return response
        response = Response()
        response.data = {
            "access": str(refresh.access_token),
        }
        set_refresh_cookie(response, str(refresh))
        return response
