from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout

from .serializers import SignUpSerializer


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

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
            token, created = Token.objects.get_or_create(user=user)
            response = {
                "user": str(user.get_username()),
                "token": user.get_session_auth_hash(),
                "auth_token": token.key,
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request: Request) -> Response:
        content = {"user": str(request.user), "token": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
