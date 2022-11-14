from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.PostCreate.as_view()),
    path('mine/',views.get_my_post),
    path('<str:uid>/',views.PostDetail.as_view()),
    # path('<str:uid>/update/',views.PostUpdate.as_view()),
    path('',views.PostList.as_view()),
    path('category/<str:uid>/',views.get_posts_by_category),
]
