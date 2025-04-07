from django.urls import path

from .views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDeleteAPIView,
    UserPostListAPIView,
)

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post_list_create"),
    path(
        "<int:pk>/",
        PostRetrieveUpdateDeleteAPIView.as_view(),
        name="post_retrieve_update_delete",
    ),
    path("current_user/", UserPostListAPIView.as_view(), name="current_user"),
]
