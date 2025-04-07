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

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

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

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


# class UserPostListAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserPostSerializer
#
#     def get(self, request: Request, *args, **kwargs) -> Response:
#         user = self.request.user
#         serializer = self.serializer_class(instance=user)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserPostListCreateAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(author=user)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)
