from rest_framework import serializers
from .models import Post
from common.serializers import CategorySerializer

class PostSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(many=True,read_only=True)
    class Meta:
        model = Post
        # fields='__all__'
        exclude =['views']
