from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate, login, logout

from .serializers import SignUpSerializer, LoginSerializer


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Signup a new user account",
        operation_description="This endpoint signs up a new user",
    )
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
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login an user and generate token",
        operation_description="This endpoint logins a user and generates a token",
    )
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer["email"]
            password = serializer["password"]

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
                data={"message": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
