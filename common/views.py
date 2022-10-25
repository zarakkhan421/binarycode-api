from django.shortcuts import render
from .serializers import CategorySerializer
from rest_framework import generics
from .models import Category
from rest_framework import permissions
from common import permissions as customPermissions
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostSerializer, serializers

# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[]
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Category.objects.all()
    lookup_field='uid'
    serializer_class=CategorySerializer
    permission_classes=[]
    
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     uid = self.kwargs['uid']
    #     posts = Post.objects.filter(category_id=uid)
    #     posts = PostSerializer(data=posts,many=True)
    #     posts.is_valid()
    #     print(posts)
    #     print(uid)
    #     serializer = self.get_serializer(instance)
    #     return Response(posts.data)
    #     # return Response()
    
    