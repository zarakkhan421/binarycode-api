from django.urls import path
from . import views

urlpatterns = [
    path('',views.CategoryList.as_view()),
    path('<str:uid>/',views.CategoryDetail.as_view())   
]
