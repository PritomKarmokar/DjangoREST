from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status, generics, mixins

from .models import Post
from .serializers import PostSerializer

#
# class PostViewSet(viewsets.ViewSet):
#     serializer_class = PostSerializer
#
#     def list(self, request: Request) -> Response:
#         queryset = Post.objects.all().order_by("-created_at")
#         serializer = self.serializer_class(instance=queryset, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def retrieve(self, request: Request, pk=None) -> Response:
#         post = get_object_or_404(Post, pk=pk)
#         serializer = self.serializer_class(instance=post)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
