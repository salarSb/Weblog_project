from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles-list'),
    path('article/<int:year>/<int:month>/<int:day>/<slug:article>', views.article_detail, name='article-detail'),
    path('create-article/', views.CreateArticleView.as_view(), name='create-article'),
]
