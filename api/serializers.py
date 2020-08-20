from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user = User.objects.all()
        model = User
        fields = '__all__'


class UserBodySerializer(serializers.Serializer):
    name = serializers.CharField(help_text="닉넴")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        post = Post.objects.all()
        model = Post
        fields = '__all__'


class PostBodySerializer(serializers.Serializer):
    title = serializers.CharField(help_text="제목")