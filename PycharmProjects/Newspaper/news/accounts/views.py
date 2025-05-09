from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .mixins import AutoGroupMixin
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import Group, User
from .forms import UserRegistrationForm, BecomeAuthorForm, UsernameChangeForm
from info.models import Post, Article, Category, PostCategory, Author
from django.db.models import Count, IntegerField, F, Q, Exists, OuterRef
from django.db.models.functions import Coalesce


@login_required
def profile(request):
    is_author = request.user.groups.filter(name='Authors').exists()
    username_form = UsernameChangeForm(instance=request.user)
    message = None

    if request.method == 'POST' and 'change_username' in request.POST:
        username_form = UsernameChangeForm(request.POST, instance=request.user)
        if username_form.is_valid():
            username_form.save()
            message = 'Имя пользователя успешно изменено!'
            username_form = UsernameChangeForm(instance=request.user)

    # Лидерборд
    leaderboard = User.objects.filter(
        groups__name='Authors'
    ).annotate(
        post_count=Count('posts', distinct=True),
        article_count=Count('articles', distinct=True),
        total_pubs=F('post_count') + F('article_count')
    ).filter(
        total_pubs__gt=0
    ).order_by('-total_pubs')[:5]

    # Статистика пользователя
    user_position = None
    user_stats = {}
    if is_author:
        post_count = request.user.posts.count()
        article_count = request.user.articles.count()
        total_pubs = post_count + article_count

        user_stats = {
            'total_pubs': total_pubs,
            'news_count': post_count,
            'articles_count': article_count
        }

        user_position = User.objects.filter(
            groups__name='Authors'
        ).annotate(
            total=Count('posts', distinct=True) + Count('articles', distinct=True)
        ).filter(
            total__gt=total_pubs
        ).count() + 1

    # Подписки пользователя
    user_categories = Category.objects.filter(
        subscribers=request.user
    ).annotate(
        articles_count=Count('articles', distinct=True)
    )

    # Все категории с информацией о подписке
    all_categories = Category.objects.annotate(
        posts_count=Count('articles', distinct=True),
    ).annotate(
        is_subscribed=Exists(
            Category.objects.filter(
                id=OuterRef('pk'),
                subscribers=request.user
            )
        )
    ).order_by('name')

    context = {
        'is_author': is_author,
        'leaderboard': leaderboard,
        'user_position': user_position,
        'user_stats': user_stats,
        'username_form': username_form,
        'message': message,
        'user_categories': user_categories,
        'all_categories': all_categories,
    }
    return render(request, 'accounts/profile.html', context)
@login_required
def become_author(request):
    if request.method == 'POST':
        form = BecomeAuthorForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            authors_group, created = Group.objects.get_or_create(name='Authors')  # Безопасное получение группы
            request.user.groups.add(authors_group)
            return redirect('profile')
    else:
        form = BecomeAuthorForm()

    return render(request, 'accounts/become_author.html', {'form': form})

class RulesView(TemplateView):
    template_name = 'accounts/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rules'] = [
            "Вы умеете писать 'мама', 'папа' и 'гидронасоснотрехфакторная теплоэлектростанция'",
            "Вы дышите",
        ]
        return context


@login_required
def change_username(request):
    message = None
    message_type = 'success'

    if request.method == 'POST':
        new_username = request.POST.get('new_username', '').strip()

        # Валидация
        if not new_username:
            message = 'Пожалуйста, введите новое имя пользователя'
            message_type = 'error'
        elif User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
            message = 'Это имя пользователя уже занято'
            message_type = 'error'
        else:
            # Сохраняем изменения
            request.user.username = new_username
            request.user.save()
            message = 'Имя пользователя успешно изменено!'

            # Выход пользователя для применения изменений
            from django.contrib.auth import logout
            logout(request)
            return redirect('account_login')  # Перенаправляем на страницу входа

    return render(request, 'accounts/change_username.html', {
        'message': message,
        'message_type': message_type,
    })





