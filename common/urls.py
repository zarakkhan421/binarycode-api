from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/',views.UserLoginView.as_view()),
    path('logout/',views.UserLogoutView.as_view()),
    path('change/password/',views.UserChangePasswordView.as_view()),
    path('reset/email/',views.SendPasswordResetEmailView.as_view()),
    path('reset/password/<uid>/<token>/',views.UserPasswordResetView.as_view()),
    path('',views.CategoryList.as_view()),
    path('<str:uid>/',views.CategoryDetail.as_view()),
]
