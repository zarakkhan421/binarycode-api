from rest_framework import serializers
from .models import Post
from common.serializers import CategorySerializer
from common.serializers import UserSerializer
# from comment.serializers import CommentListPerPostSerializer

class PostSerializer(serializers.ModelSerializer):
    # category_id = CategorySerializer(many=True,read_only=True)
    # user_id = UserSerializer(read_only=True)
    class Meta:
        model = Post
        # fields='__all__'
        exclude =['views']
class PostCreateSerializer(serializers.ModelSerializer):
    # category_id = CategorySerializer(many=True,read_only=True)
    # user_id = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields='__all__'
        # exclude =['views']

class PostListSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(many=True,read_only=True)
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields='__all__'
        # exclude =['views']
class PostDetailSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(many=True,read_only=True)
    user_id = UserSerializer(read_only=True)
    # comments = CommentListPerPostSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields='__all__'
        # exclude =['views']
