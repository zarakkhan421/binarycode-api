from django.shortcuts import render
from .serializers import CategorySerializer
from rest_framework import generics
from .models import Category
from rest_framework import permissions
from common import permissions as customPermissions
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostSerializer
from common.serializers import UserRegistrationSerializer, UserLoginSerializer,UserChangePasswordSerializer, SendPasswordResetEmailSerializer,UserPasswordResetSerializer, CustomTokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from common.renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .serializers import CookieTokenRefreshSerializer
from django.conf import settings

from rest_framework_simplejwt.views import TokenVerifyView
# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
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
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

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
      response.set_cookie(key='refresh_token',value=token['refresh'], max_age=cookie_max_age, httponly=True)
      response.data ={'token':token, 'msg':'Login Success'}
      response.status_code=status.HTTP_200_OK
      return response
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = settings.COOKIE_AGE
            response.set_cookie(key='refresh_token', value=response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)


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