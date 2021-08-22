from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from articles.models import Article


class LatestArticlesFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('articles:articles-list')
    description = 'New Articles of my Blog'

    def items(self):
        return Article.objects.published_articles()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
