from base64 import decode
from os import access
from urllib import response
from django.shortcuts import render
from .serializers import CategorySerializer
from rest_framework import generics
from .models import Category
from rest_framework import permissions
from common import permissions as customPermissions
from rest_framework.response import Response
from post.models import Post
from common.serializers import UserRegistrationSerializer, UserLoginSerializer,UserChangePasswordSerializer, SendPasswordResetEmailSerializer,UserPasswordResetSerializer, CustomTokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from common.renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# from .serializers import CookieTokenRefreshSerializer
from django.conf import settings
from rest_framework.decorators import api_view
from common import serializers
from rest_framework_simplejwt import views
from rest_framework_simplejwt.views import TokenVerifyView
from decouple import config
from rest_framework.decorators import api_view
from django.http import Http404
from common.models import User
from django.db.models import Q
from post.serializers import PostListSerializer

# Create your views here.
@api_view(['GET'])
def search(requset,query):
  posts = Post.objects.filter(Q(title__icontains =query)| Q(content__icontains =query))
  serializer = PostListSerializer(posts,many=True)
  print(serializer.data)
  return Response(serializer.data,status=status.HTTP_200_OK)

class CategoryList(generics.ListCreateAPIView):
    queryset=Category.objects.filter(parent__isnull=True)
    serializer_class=CategorySerializer
    permission_classes=[customPermissions.POSTCategoryPermissions]
    
    def get_serializer_class(self):
        print(self.request.method)
        if(self.request.method) == 'POST':
            print('we here')
            return serializers.CategoryCreateSerializer
        else:
            print('no here')
            return serializers.CategorySerializer
                     
class CategoryListAll(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=serializers.CategoryParentSerializer
    permission_classes=[customPermissions.POSTCategoryPermissions]
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Category.objects.all()
    lookup_field='uid'
    serializer_class=CategorySerializer
    permission_classes=[customPermissions.ObjectCategoryPermissions]



def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'role':user.role,'email':user.email,'msg':'registration success', 'user_id':user.uid}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    response = Response()
    print(response)
    if user is not None:
      token = get_tokens_for_user(user)
      cookie_max_age = settings.COOKIE_AGE
      response.set_cookie(key='refresh_token',value=token['refresh'], max_age=cookie_max_age,samesite='None', secure=False, httponly=True)
      response.set_cookie(key='access_token',value=token['access'], max_age=cookie_max_age,samesite='None', secure=False, httponly=True)
      user_id = str(user.uid)
      response.data ={'token':token,'role':user.role,"email":user.email,'user_id':user_id, 'msg':'Login Success'}
      response.status_code=status.HTTP_200_OK
      return response
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
  def post(self,request):
    response = Response()
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    response.status_code=status.HTTP_200_OK
    response.data={
      'message':'logged out'
    }
    return response
    
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
  
  
class EditUserView(APIView):
    # queryset= Category.objects.all()
    # lookup_field='uid'
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    # serializer_class = serializers.UserSerializer
     def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
          
     def patch(self,request):
        user = self.get_object(request.user.uid)
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    # queryset= Category.objects.all()
    # lookup_field='uid'
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    # serializer_class = serializers.UserSerializer
     def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
          
     def get(self, request, uid, format=None):
        user = self.get_object(uid)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class CustomTokenVerifyView(TokenVerifyView):
     serializer_class=CustomTokenVerifySerializer
     
     
class RefreshAccessToken(APIView):
  def post(self,request):
    print(request.COOKIES)
    print('sdsvfereg534')
    return Response({'data':'gone'})

class CustomTokenRefreshView(views.TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = serializers.CustomTokenRefreshSerializer