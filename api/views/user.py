from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers import UserSerializer


class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Passwords must match")

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(User.objects.all(), many=True).data
        return Response(data)


class UserDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user).data
        return Response(data)
