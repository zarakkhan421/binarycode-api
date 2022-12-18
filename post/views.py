from pprint import pprint
from django.shortcuts import render
import jwt
# from comment import serializers
from post import serializers
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
import pprint
from decouple import config
from rest_framework import mixins,status
from common import paginations

# Create your views here.

class PostList(generics.ListAPIView):
    queryset=Post.objects.all()
    serializer_class=serializers.PostListSerializer
    pagination_class = paginations.Pagination
    
class PostCreate(generics.CreateAPIView):
    queryset=Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes=[customPermissions.POSTPermissions]
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Post.objects.all()
    lookup_field='uid'
    # serializer_class=serializers.PostDetailSerializer
    permission_classes=[customPermissions.ObjectPermissions]
    print('this called')
    def get_serializer_class(self):
        print(self.request.method)
        if(self.request.method in ['PATCH','PUT']):
            print('we here')
            return serializers.PostCreateSerializer
        else:
            print('no here')
            return serializers.PostDetailSerializer


# class PostUpdate(generics.UpdateAPIView):
#     queryset= Post.objects.all()
#     lookup_field='uid'
#     serializer_class=serializers.PostCreateSerializer
#     permission_classes=[customPermissions.ObjectPermissions]
    


class GetPostsByCategory(APIView):
    def get(self, request,uid, *args, **kwargs):
        category = Category.objects.get(pk=uid)
        serializer = serializers.PostListSerializer(category.posts.all(),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
 
# @api_view(['GET'])
# def get_posts_by_category(request,uid):
    
#     category = Category.objects.get(pk=uid)
#     print(category.posts.all())
#     serializer = serializers.PostListSerializer(data=category.posts.all(),many=True)
#     serializer.is_valid()
#     print(serializer.data)
#     return Response(serializer.data)

@api_view(['GET'])
def get_my_post(request):
    print(request.user)
    # posts = Post.objects.all().filter(user_id=request.user.uid)
    # serializer=serializers.PostListSerializer(data=posts,many=True)
    # serializer.is_valid()
    # check
    return Response('sd')
    return Response(serializer.data)