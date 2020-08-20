from django.urls import path
from django.conf import settings

from .views import *

urlpatterns = [
    path("v1/user", UserViewSet.as_view({"get": "list", "post": "create"}), name="users"),
    path("v1/user/<int:user_id>/post", PostViewSet.as_view({"get": "list", "post": "create"}), name="posts"),
    path("v1/user/<int:user_id>/post/<int:post_id>", PostViewSet.as_view({"get": "retrieve", "put": "update"}), name="post"),
]
