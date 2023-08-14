from django.urls import path

from .views import PostsList, PostDetail

urlpatterns = [
    path("news/", PostsList.as_view()),
    path("news/<int:pk>", PostDetail.as_view()),



]