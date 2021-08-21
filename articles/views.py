from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from articles.forms import EmailPostForm
from articles.models import Article


class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.published_articles()
    paginate_by = 3
    extra_context = {
        'page_title': 'Articles'
    }


def article_detail(request, year, month, day, article):
    post = get_object_or_404(Article,
                             slug=article,
                             status='PUBLISHED',
                             publish__year=year,
                             publish__month=month,
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


def post_share(request, article_id):
    article = get_object_or_404(Article, id=article_id, status='PUBLISHED')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']} recommends you read {article.title}"
            message = f"Read {article.title} at {article_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'salarsabeti88@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'articles/share.html',
                  {'article': article, 'form': form, 'sent': sent, 'page_title': 'Send Email'})
