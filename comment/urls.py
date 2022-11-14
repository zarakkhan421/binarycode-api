from django.urls import path
from . import views
urlpatterns = [
    path('',views.comment_list),
    path('<str:uid>/',views.delete_comment),
    # path('',views.CommentList.as_view()),
    path('<str:uid>/',views.CommentDetail.as_view())
]
