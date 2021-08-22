from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from taggit.models import Tag

from articles.forms import EmailPostForm, CommentForm, SearchForm
from articles.models import Article


def article_list(request, tag_slug=None):
    object_list = Article.objects.published_articles()
    tags = Tag.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)  # 3 articles in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request, 'articles/article_list.html', {'page': page,
                                                          'articles': articles,
                                                          'tag': tag,
                                                          'tags': tags})


def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article,
                                slug=article,
                                status='PUBLISHED',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current article to the comment
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar articles
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Article.objects.published_articles().filter(tags__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {'object': article,
               'page_title': article.title,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form,
               'similar_articles': similar_articles}
    return render(request, 'articles/article_detail.html', context)


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'slug', 'body', 'publish', 'image', 'status', 'tags')
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


@csrf_exempt
@require_POST
def post_like(request, article_id):
    article = get_object_or_404(klass=Article, pk=article_id)
    article.likes += 1
    article.save()
    return JsonResponse({'success': True, 'likes': article.likes}, status=201)


def article_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Article.objects.published_articles() \
                .annotate(rank=SearchRank(search_vector, search_query)) \
                .filter(rank__gte=0.3).order_by('-rank')
    context = {'form': form,
               'query': query,
               'results': results,
               'page_title': 'Search'}
    return render(request, 'articles/search.html', context)
