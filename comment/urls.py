from django.urls import path
from . import views
urlpatterns = [
    path('<str:uid>/',views.CommentDetail.as_view()),
    path('',views.CommentList.as_view()),
    # path('<str:uid>/',views.delete_comment),
    path('post/<str:uid>/',views.comments_by_post)
    # path('',views.CommentList.as_view()),
]
