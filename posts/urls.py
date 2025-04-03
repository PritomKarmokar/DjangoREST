from django.urls import path

from .views import (
    homepage,
    list_posts,
    post_detail,
    create_post,
    update_post,
    delete_post,
)

urlpatterns = [
    path("homepage/", homepage, name="posts_home"),
    path("list/", list_posts, name="posts_list"),
    path("<int:post_id>/", post_detail, name="posts_detail"),
    path("create/", create_post, name="posts_create"),
    path("update/<int:post_id>/", update_post, name="posts_update"),
    path("delete/<int:post_id>/", delete_post, name="posts_delete"),
]
