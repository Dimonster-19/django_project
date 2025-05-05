from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Article, Category, PostCategory
from django.contrib import messages
from django.db import models
from django.db.models import Count, Q
from .forms import PostForm, ArticleForm, NewsSearchForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from itertools import chain
from django.http import JsonResponse
import logging

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
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all()
    })

def article_list(request):
    category_name = request.GET.get('category')
    articles = Article.objects.all()

    if category_name:
        articles = articles.filter(categories__name=category_name)

    all_categories = Category.objects.annotate(article_count=Count('articles'))
    articles = articles.order_by('-pub_date')

    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles.html', {
        'page_obj': page_obj,
        'all_categories': all_categories,
        'current_category': category_name
    })

def news_detail(request, news_id):
    post = get_object_or_404(Post, pk=news_id)
    return render(request, 'news_detail.html', {'post': post})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article_detail.html', {'article': article})


def news_search(request):
    form = NewsSearchForm(request.GET or None)
    content_type = request.GET.get('content_type', 'all')

    # Базовые querysets
    posts = Post.objects.all()
    articles = Article.objects.all()

    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date_after = form.cleaned_data.get('date_after')
        date_before = form.cleaned_data.get('date_before')

        # Фильтрация по заголовку
        if title:
            posts = posts.filter(title__icontains=title)
            articles = articles.filter(title__icontains=title)

        # Фильтрация по автору (исправленная версия)
        if author:
            posts = posts.filter(
                Q(author__username__icontains=author) |
                Q(author__first_name__icontains=author) |
                Q(author__last_name__icontains=author)
            )
            articles = articles.filter(
                Q(author__username__icontains=author) |
                Q(author__first_name__icontains=author) |
                Q(author__last_name__icontains=author)
            )

        # Фильтрация по дате
        if date_after:
            posts = posts.filter(created_at__gte=date_after)
            articles = articles.filter(pub_date__gte=date_after)

        if date_before:
            posts = posts.filter(created_at__lte=date_before)
            articles = articles.filter(pub_date__lte=date_before)

    # Применение фильтра по типу контента
    if content_type == 'news':
        results = posts
    elif content_type == 'articles':
        results = articles
    else:
        results = list(posts) + list(articles)

    # Сортировка
    if isinstance(results, list):
        results.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') else x.pub_date, reverse=True)
    else:
        results = results.order_by('-created_at') if content_type == 'news' else results.order_by('-pub_date')

    # Пагинация
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news_search.html', {
        'form': form,
        'results': page_obj,
        'content_type': content_type,
        'request': request
    })


from django.shortcuts import redirect


# views.py
def create_news(request):
    if request.method == "POST":
        form = PostForm(request.POST, request=request)

        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = request.user
                post.type = Post.NEWS
                post.save()  # Сначала сохраняем пост
                form.save_m2m()  # Затем сохраняем категории

                messages.success(request, 'Новость успешно опубликована!')
                return redirect('news')

            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле "{field}": {error}')
    else:
        form = PostForm(request=request)

    return render(request, 'create.html', {
        'form': form,
        'title': 'Создание новости'
    })



logger = logging.getLogger(__name__)

def edit_news(request, news_id):
    news_item = get_object_or_404(Post, id=news_id)

    # Проверка прав
    if not (request.user.is_superuser or request.user == news_item.author):
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(request.POST, instance=news_item, request=request)

        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.save()
                form.save_m2m()

                messages.success(request, 'Изменения успешно сохранены!')
                return JsonResponse({'success': True})

            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
                logger.error(f"Error saving post: {str(e)}")
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        else:
            errors = {f: [str(e) for e in err] for f, err in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = PostForm(instance=news_item, request=request)

    return render(request, 'edit_news.html', {
        'form': form,
        'news_item': news_item,
        'title': f'Редактирование: {news_item.title}'
    })

def delete_news(request, news_id):
    news_item = get_object_or_404(Post, id=news_id)
    if request.method == "POST":
        news_item.delete()
        return redirect('news')  # Перенаправление на список новостей
    return render(request, 'news_delete.html', {'object': news_item})


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            form.save_m2m()  # Важно для сохранения категорий
            return redirect('articles')
    else:
        form = ArticleForm(initial={'author': request.user})

    return render(request, 'article_create.html', {'form': form})


def article_search(request):
    query = request.GET.get('q', '')
    articles = Article.objects.all()

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(articles.order_by('-pub_date'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'article_search.html', {
        'page_obj': page_obj,
        'search_query': query
    })


def author_required(user):
    """Проверка, что пользователь в группе Authors или является суперпользователем"""
    return user.groups.filter(name='Authors').exists() or user.is_superuser


@login_required
@user_passes_test(author_required)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            form.save_m2m()  # Сохраняем изменения в категориях
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'article_edit.html', {
        'form': form,
        'article': article
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


def category_news(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    news_in_category = Post.objects.filter(categories=category)
    articles_in_category = Article.objects.filter(categories=category)

    # Добавляем правильное поле даты для каждого объекта
    combined = []
    for item in chain(news_in_category, articles_in_category):
        if hasattr(item, 'created_at'):  # Для новостей
            item.sort_date = item.created_at
        elif hasattr(item, 'pub_date'):  # Для статей
            item.sort_date = item.pub_date
        combined.append(item)

    # Сортируем по добавленному полю sort_date
    combined_sorted = sorted(combined, key=lambda obj: obj.sort_date, reverse=True)

    return render(request, 'news.html', {
        'page_obj': combined_sorted,
        'selected_category': category,
    })


@login_required
def subscribe_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на категорию "{category.name}"')
    return redirect('articles')

@login_required
def unsubscribe_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    messages.success(request, f'Вы отписались от категории "{category.name}"')
    return redirect('articles')