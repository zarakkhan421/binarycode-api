from django.shortcuts import render

from comment import serializers
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .models import Post
from rest_framework import permissions
from common import permissions as customPermissions
from rest_framework import mixins
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from common.models import Category

# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,customPermissions.ListPermissions]
    
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView, mixins.RetrieveModelMixin):
    queryset= Post.objects.all()
    lookup_field='uid'
    serializer_class=PostSerializer
    permission_classes = [customPermissions.DetailPermissons]
    


@api_view(['GET'])
def get_posts_by_category(request,uid):
    category = Category.objects.get(pk=uid)
    print(category.posts.all())
    serializer = PostSerializer(data=category.posts.all(),many=True)
    serializer.is_valid()
    print(serializer.data)
    return Response(serializer.data)