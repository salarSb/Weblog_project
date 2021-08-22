from django.contrib.sitemaps import Sitemap

from articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.published_articles()

    def lastmod(self, obj):
        return obj.updated
