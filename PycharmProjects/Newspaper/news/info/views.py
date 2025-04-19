from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Article
from django.contrib import messages
from django.db.models import Q
from .forms import PostForm, ArticleForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Использование class-based views:
class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5  # Установка 5 статей на страницу

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = "post"

# Использование function-based views:
def news_list(request):
    news = Post.objects.all().order_by('-created_at')
    paginator = Paginator(news, 5)  # Показывать 5 новостей на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj})

def article_list(request):
    articles = Article.objects.all().order_by('-pub_date')
    paginator = Paginator(articles, 5)  # Показывать 5 статей на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'articles.html', {'page_obj': page_obj})


def news_detail(request, news_id):
    post = get_object_or_404(Post, pk=news_id)
    return render(request, 'news_detail.html', {'post': post})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article_detail.html', {'article': article})


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        title_query = self.request.GET.get('title', '')
        author_query = self.request.GET.get('author', '')
        date_query = self.request.GET.get('date', '')

        # Обработка ошибок
        try:
            # Фильтрация по критериям
            if title_query:
                queryset = queryset.filter(title__icontains=title_query)
            if author_query:
                queryset = queryset.filter(author__name__icontains=author_query)
            if date_query:
                queryset = queryset.filter(created_at__gt=date_query)
        except Exception as e:
            messages.error(self.request, "Ошибка в параметрах поиска. Пожалуйста, проверьте введенные данные.")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def create_news(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})

def edit_news(request, news_id):
    news_item = get_object_or_404(Post, id=news_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = PostForm(instance=news_item)

    return render(request, 'edit_news.html', {'form': form, 'news_item': news_item})

def delete_news(request, news_id):
    news_item = get_object_or_404(Post, id=news_id)
    if request.method == "POST":
        news_item.delete()
        return redirect('news')
    return render(request, 'confirm_delete.html', {'object': news_item})

def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm()
    return render(request, 'article_create.html', {'form': form})




def author_required(user):
    """Проверка, что пользователь в группе Authors или является суперпользователем"""
    return user.groups.filter(name='Authors').exists() or user.is_superuser

@login_required
@user_passes_test(author_required)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Дополнительная проверка, что пользователь - автор статьи
    if request.user != article.author and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('article_detail', article_id=article.id)  # Перенаправляем на просмотр статьи
    else:
        form = ArticleForm(instance=article)

    return render(request, 'article_edit.html', {
        'form': form,
        'article': article,
        'title': 'Редактирование статьи'
    })


@login_required
@user_passes_test(author_required)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Дополнительная проверка, что пользователь - автор статьи
    if request.user != article.author and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        article.delete()
        messages.success(request, 'Статья успешно удалена')
        return redirect('articles')  # Или другой подходящий URL

    return render(request, 'confirm_delete.html', {
        'object': article,
        'title': 'Подтверждение удаления статьи'
    })


def hello(request):
    return render(request, 'hello.html')