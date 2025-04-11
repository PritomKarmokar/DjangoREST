from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post
from posts.views import PostListCreateAPIView

User = get_user_model()


class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("home"))

        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Currently, Available Posts")


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("post_list_create")
        self.authenticate_user()

    def authenticate_user(self):
        signup_response = self.client.post(
            reverse("signup"),
            {"username": "testuser", "password": "test123", "email": "test@gmail.com"},
        )
        print(signup_response)

        response = self.client.post(
            reverse("login"),
            {"email": "test@gmail.com", "password": "test123"},
        )
        print(response.content)

        token = response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_posts(self):
        response = self.client.get(
            self.url,
        )
        print(f"response.data : {response.data}")
        # print(f"response.content : {response.content}") # It returns response in the 'byte format'

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        sample_post = {
            "title": "Test Post",
            "content": "Test Post",
        }
        create_response = self.client.post(
            reverse("post_list_create"),
            sample_post,
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
