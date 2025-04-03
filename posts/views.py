from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post
from .serializers import PostSerializer


@api_view(http_method_names=["GET", "POST"])
def homepage(request: Request) -> Response:
    if request.method == "GET":
        response = {"message": "hello, world"}
        return Response(response, status=status.HTTP_200_OK)
    else:
        data = request.data
        response = {"message": data}
        return Response(response, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def list_posts(request: Request) -> Response:
    posts = Post.objects.all().order_by("-created_at")
    serializer = PostSerializer(instance=posts, many=True)
    response = {
        "message": "Currently Available Posts",
        "posts": serializer.data,
    }
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
def create_post(request: Request) -> Response:
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "New Post Created Successfully",
            "post": serializer.data,
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET"])
def post_detail(request: Request, post_id: int) -> Response:
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(instance=post)
        response = {
            "message": f"Details of Post with ID {post_id} exist",
            "post": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    except Post.DoesNotExist:
        response = {
            "message": f"Post with the following ID {post_id} does not exist",
        }
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {str(e)}",
        }
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=["PATCH"])
def update_post(request: Request, post_id: int) -> Response:
    try:
        data = request.data
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(instance=post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": f"Post with the Id {post_id} Updated Successfully",
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        response = {
            "message": f"Post with the following ID {post_id} does not exist",
        }
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {str(e)}",
        }
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=["DELETE"])
def delete_post(request: Request, post_id: int) -> Response:
    return Response(status=status.HTTP_200_OK)
