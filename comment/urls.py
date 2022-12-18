from django.urls import path
from . import views
urlpatterns = [
    path('<str:uid>/',views.CommentDetail.as_view()),
    path('all',views.CommentList.as_view()),
    path('',views.CommentPost.as_view()),
    path('post/<str:uid>/',views.comments_by_post)
]
