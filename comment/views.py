from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework import generics
from .models import Comment
from rest_framework import permissions
from common import permissions as customPermissons

# Create your views here.

class CommentList(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[]
    
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='uid'
    permission_classes=[]