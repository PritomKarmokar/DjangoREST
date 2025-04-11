from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout

from .serializers import SignUpSerializer


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "New User Created, successfully",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request: Request) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            response = {
                "user": f"{user.get_username()} logged in successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request: Request) -> Response:
        content = {"user": str(request.user), "token": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
