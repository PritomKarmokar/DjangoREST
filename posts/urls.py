from django.urls import path

from .views import PostListCreateAPIView, PostRetrieveUpdateDeleteAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post_list_create"),
    path(
        "<int:post_id>/",
        PostRetrieveUpdateDeleteAPIView.as_view(),
        name="post_retrieve_update_delete",
    ),
]
