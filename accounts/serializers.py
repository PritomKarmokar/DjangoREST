from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from posts.serializers import PostSerializer
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been taken")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user


class UserPostSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "posts"]

    def get_posts(self, obj):
        posts = obj.posts.all()
        return PostSerializer(posts, many=True).data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=5)
