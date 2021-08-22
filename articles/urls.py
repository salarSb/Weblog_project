from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='articles-list'),
    path('tag/<slug:tag_slug>', views.article_list, name='articles_list_by_tag'),
    path('article/<int:year>/<int:month>/<int:day>/<slug:article>', views.article_detail, name='article-detail'),
    path('create-article/', views.CreateArticleView.as_view(), name='create-article'),
    path('share/<int:article_id>/', views.post_share, name='article-share'),
    path('like/<int:article_id>', views.post_like, name='article-like'),
    path('feed/', LatestArticlesFeed(), name='article-feed'),
    path('search/', views.article_search, name='article-search'),
]
