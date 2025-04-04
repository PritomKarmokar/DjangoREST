from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView

from .models import Post
from .serializers import PostSerializer


class PostAPIBaseView(APIView):
    serializer_class = PostSerializer

    def format_response(
        self, message, data=None, errors=None, status_code=status.HTTP_200_OK
    ) -> Response:
        response = {
            "message": message,
            "data": data,
            "errors": errors,
        }
        return Response(response, status=status_code)

    def get_post(self, post_id: int) -> Post:
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return None


class PostListCreateAPIView(PostAPIBaseView):
    """
    A view for creating and listing posts
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        all_posts = Post.objects.all().order_by("-created_at")
        serializer = self.serializer_class(instance=all_posts, many=True)

        return self.format_response(
            message="Available posts",
            data=serializer.data,
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return self.format_response(
                message="New Post Created Successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )

        return self.format_response(
            message="Validation Failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class PostRetrieveUpdateDeleteAPIView(PostAPIBaseView):
    """
    A view for retrieving, updating and deleting a post
    """

    def get(self, request: Request, post_id: int, *args, **kwargs) -> Response:

        post = self.get_post(post_id)
        if not post:
            return self.format_response(
                message=f"Post with the following ID {post_id} does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(instance=post)
        return self.format_response(
            message=f"Details of Post with ID {post_id} retrieved successfully",
            data=serializer.data,
        )

    def patch(self, request: Request, post_id: int, *args, **kwargs) -> Response:
        data = request.data
        post = self.get_post(post_id)
        if not post:
            return self.format_response(
                message=f"Post with the following ID {post_id} does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(instance=post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.format_response(
                message=f"Post with the Id {post_id} Updated Successfully",
                data=serializer.data,
            )
        else:
            return self.format_response(
                message=f"Validation Failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request: Request, post_id: int, *args, **kwargs) -> Response:
        post = self.get_post(post_id)
        if not post:
            return self.format_response(
                message=f"Post with the following ID {post_id} does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        post.delete()
        return self.format_response(
            message=f"Post with the Id {post_id} Deleted Successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )
