from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import Post, Category
from datetime import timedelta
from django.utils import timezone


@shared_task
def send_weekly_newsletter():
    # Получаем новости за последнюю неделю
    last_week = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(
        created_at__gte=last_week,
        type=Post.NEWS
    ).order_by('-created_at')

    # Если нет новых новостей - выходим
    if not recent_posts.exists():
        return "No new posts this week"

    # Для каждой категории собираем подписчиков
    categories = Category.objects.prefetch_related('subscribers').all()

    for category in categories:
        # Фильтруем новости по категории
        category_posts = recent_posts.filter(categories=category)
        if not category_posts.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        for subscriber in subscribers:
            if not subscriber.email:
                continue

            # Формируем контекст для шаблона
            context = {
                'user': subscriber,
                'posts': category_posts,
                'category': category,
                'domain': getattr(settings, 'DOMAIN', 'example.com'),
                'site_name': getattr(settings, 'SITE_NAME', 'Мой сайт')
            }

            # Рендерим письмо
            html_message = render_to_string(
                'account/email/weekly_newsletter.html',
                context
            )
            plain_message = strip_tags(html_message)

            # Отправляем письмо
            send_mail(
                subject=f'Еженедельная подборка новостей в категории "{category.name}"',
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False
            )

    return f"Sent weekly newsletter with {recent_posts.count()} posts"