from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from articles.models import Article


class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.published_articles()
    paginate_by = 6
    extra_context = {
        'page_title': 'Articles'
    }


def article_detail(request, year, month, day, article):
    post = get_object_or_404(Article, slug=article, status='PUBLISHED', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'articles/article_detail.html', {'object': post, 'page_title': post.title})


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'slug', 'body', 'image', 'status')
    success_url = reverse_lazy('articles:articles-list')
    extra_context = {
        'page_title': 'Create Article'
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateArticleView, self).form_valid(form)
