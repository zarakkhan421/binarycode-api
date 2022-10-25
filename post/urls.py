from django.urls import path
from . import views

urlpatterns = [
    path('',views.PostList.as_view()),
    path('<str:uid>/',views.PostDetail.as_view()),
    path('category/<str:uid>/',views.get_posts_by_category)
]
