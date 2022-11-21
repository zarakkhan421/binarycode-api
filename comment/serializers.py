# from dataclasses import field
# from pyexpat import model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from common.serializers import UserSerializer
from post.serializers import PostSerializer
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
class CommentNestedPostSerializer(serializers.ModelSerializer):
    # from post.serializers import PostDetailSerializer
    replies=RecursiveField(many=True)
    user_id = UserSerializer(read_only=True)
    post_id =PostSerializer(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'
        