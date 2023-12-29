from django.urls import path

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete
from .views import ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete
from .views import ChoicePost, subscriptions
#from .views import IndexView #celery
urlpatterns = [

    path("news/", PostsList.as_view(), name="post_list"),
    path("news/<int:pk>", PostDetail.as_view(), name='post_detail'),
    path("news/create/", PostCreate.as_view(), name="post_create"),
    path("news/<int:pk>/update/", PostUpdate.as_view(), name="post_update"),
    path("news/<int:pk>/delete/", PostDelete.as_view(), name="post_delete"),

    path("articles/create/", ArticleCreate.as_view(), name="article_create"),
    path("articles/", ArticlesList.as_view(), name="articles_list"),
    path("articles/<int:pk>", ArticleDetail.as_view(), name='article_detail'),
    path("articles/<int:pk>/update/", ArticleUpdate.as_view(), name="article_update"),
    path("articles/<int:pk>/delete/", ArticleDelete.as_view(), name="article_delete"),

    path("", ChoicePost.as_view(), name="choice_post"),
    path('subscriptions/', subscriptions, name='subscriptions'),



]