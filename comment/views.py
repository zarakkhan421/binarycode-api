from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework import generics
from .models import Comment
from rest_framework import permissions
from common import permissions as customPermissons
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from post.models import Post
from django.db.models import F
from comment import serializers

# Create your views here.

class CommentList(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[customPermissons.CommentPermissions]
    def post(self, request, *args, **kwargs):
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            post = Post.objects.filter(uid = serializer.data['post_id']).update(comment_count=F('comment_count')+1)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = serializers.CommentNestedPostSerializer(comments,many=True)
        print('swer5')
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    lookup_field='uid'
    permission_classes=[customPermissons.CommentPermissions]
    
    def delete(self, request,uid, *args, **kwargs):
        comment = Comment.objects.get(pk=uid)
        self.check_object_permissions(self.request,comment)
        print(request.user,request.user.role)
        serializer = CommentSerializer(comment)
        post = Post.objects.filter(uid = serializer.data['post_id']).update(comment_count=F('comment_count')-1)
        comment.delete()
        return Response({'success':'True'})
    

@api_view(['GET'])
def comments_by_post(request,uid):
    comments = Comment.objects.filter(post_id = uid,parent__isnull=True)
    serializer = serializers.CommentNestedPostSerializer(comments,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)