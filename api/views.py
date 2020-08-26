from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg.inspectors.base import openapi
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
# Create your views here.


class UserViewSet(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                View):

    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserBodySerializer)
    def create(self, request):
        user_serializer = UserSerializer(data=request.data, partial=True)
        if not user_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        user = user_serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        users = User.objects.all()

        return users


class PostViewSet(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                View):

    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostBodySerializer)
    def add(self, request, user_id):
        # django-sharding 사용 시 시리얼라이저로 save는 할 수 없음..
        post = Post(
            title=request.data['title'],
            user_id=user_id
        )

        post.save()

        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        shard = Post(user_id=user_id).get_shard()

        return Post.objects.using(shard).filter(user_id=user_id)