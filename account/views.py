from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account import serializers
from account.serializers import RegistrationSerializer, ActivationSerializer, User, LoginSerializer


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response("Successfully signed up!", status=201)


class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response("Your account successfully activated")


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response('Successfully logged out')


class ChangePasswordView(APIView):
    pass
class ForgotPassword(APIView):
    pass
