from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from taggit.managers import TaggableManager

from articles.enums import ArticleStatuses


class PublishedManager(models.Manager):
    def published_articles(self):
        return self.filter(status__startswith='PUBLISHED')


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    status = models.CharField(max_length=10, choices=ArticleStatuses.choices, default=ArticleStatuses.DRAFT)
    likes = models.IntegerField(default=0)
    objects = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('articles:article-detail',
                            args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'commented by {self.name} on {self.article}'
