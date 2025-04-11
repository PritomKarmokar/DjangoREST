from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status, generics, mixins
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from drf_yasg.utils import swagger_auto_schema

from .models import Post
from .serializers import PostSerializer
from accounts.serializers import UserPostSerializer
from .permissions import ReadOnly, AuthorOrReadOnly


class HomePageAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        response = {
            "message": "Currently, Available Posts",
            "posts": serializer.data,
        }
        return Response(data=response, status=status.HTTP_200_OK)


class PostListCreateAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """
    A view for creating and listing posts
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    @swagger_auto_schema(
        operation_summary="Listing all posts",
        operation_description="This returns a list of all posts",
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creates a new post",
        operation_description="This endpoint creates a new post",
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteAPIView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    A view for retrieving, updating and deleting a post
    """

    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    queryset = Post.objects.all()

    @swagger_auto_schema(
        operation_summary="Retrieve a post by id",
        operation_description="This endpoint retrieves a post by id",
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Updates a post by id",
        operation_description="This endpoint updates a post by id",
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs, partial=True)

    @swagger_auto_schema(
        operation_summary="Deletes a post by id",
        operation_description="This endpoint deletes a post by id",
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class UserPostListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPostSerializer

    @swagger_auto_schema(
        operation_summary="Lists post for the authenticated user",
        operation_description="This endpoint lists posts for the authenticated user",
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        user = self.request.user
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserPostListCreateAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(author=user)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)
