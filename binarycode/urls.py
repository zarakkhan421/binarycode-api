"""binarycode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from rest_framework.urlpatterns import format_suffix_patterns

# from common.views import CookieTokenRefreshView
from common.views import CustomTokenVerifyView
from common import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/',include('post.urls')),
    path('categories/',include('common.urls')),
    path('comments/',include('comment.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('api/token/renew/',views.RefreshAccessToken.as_view()),
    path('api/auth/', include('common.urls')),
    
    path('search/<str:query>/',views.search)
]
urlpatterns = format_suffix_patterns(urlpatterns)
