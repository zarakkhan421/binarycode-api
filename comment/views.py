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

# Create your views here.

class CommentList(generics.ListAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[customPermissons.ObjectPermissions]
    
 
    
@api_view(['POST',"GET"])
@permission_classes([customPermissons.POSTCommentPermissions])
def comment_list(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            post = Post.objects.filter(uid = serializer.data['post_id']).update(comment_count=F('comment_count')+1)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        comments = Comment.objects.all()
        serializers = CommentSerializer(comments,many=True)
        print('swer5')
        return Response(serializers.data,status=status.HTTP_200_OK)

class CommentDetail(generics.RetrieveUpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='uid'
    permission_classes=[customPermissons.ObjectCommentPermissions]
    
    
@api_view(['DELETE'])
@permission_classes([customPermissons.ObjectCommentPermissions])
def delete_comment(request,uid):
    comment = Comment.objects.get(pk=uid)
    serializer = CommentSerializer(comment)
    post = Post.objects.filter(uid = serializer.data['post_id']).update(comment_count=F('comment_count')-1)
    comment.delete()
    return Response({'success':'True'})