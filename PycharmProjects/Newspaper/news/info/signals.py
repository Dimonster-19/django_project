from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

from .models import Post, Article

logger = logging.getLogger(__name__)


def send_post_notification(instance, category):
    # Отладочная информация
    print(f"DEBUG: Item ID: {instance.id}")  # Проверка ID
    print(f"DEBUG: Item class: {instance.__class__.__name__}")

    # Проверка доступности URL
    try:
        from django.urls import reverse
        test_url = reverse('article_detail', args=[instance.id])
        print(f"DEBUG: Test URL: {test_url}")
    except Exception as e:
        print(f"URL ERROR: {str(e)}")

    print(f"DEBUG: Sending notification for {instance.__class__.__name__}")

    subscribers = category.subscribers.all()
    if not subscribers.exists():
        print("DEBUG: No subscribers for this category")
        return

    for subscriber in subscribers:
        print(f"DEBUG: Processing subscriber {subscriber.username}")

        if not subscriber.email:
            print(f"DEBUG: Subscriber {subscriber.username} has no email")
            continue

        is_article = isinstance(instance, Article)
        template_path = 'account/email/new_article_notification.html' if is_article else 'account/email/news_notification.html'

        print(f"DEBUG: Using template {template_path}")

        context = {
            'user': subscriber,
            'item': instance,
            'category': category,
            'domain': getattr(settings, 'DOMAIN', 'example.com'),
            'site_name': getattr(settings, 'SITE_NAME', 'Мой сайт')
        }

        try:
            html_message = render_to_string(template_path, context)
            print(f"DEBUG: Rendered template: {html_message[:100]}...")

            send_mail(
                subject=f'Новый {"материал" if is_article else "пост"} в категории "{category.name}"',
                message=strip_tags(html_message),
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False
            )
            print(f"DEBUG: Email sent to {subscriber.email}")
        except Exception as e:
            print(f"ERROR: Failed to send email: {str(e)}")


@receiver(post_save, sender=Post)
@receiver(post_save, sender=Article)
def notify_on_create(sender, instance, created, **kwargs):
    if not created:
        return
    logger.info(f"Processing new {sender.__name__}: {instance}")


@receiver(m2m_changed, sender=Post.categories.through)
@receiver(m2m_changed, sender=Article.categories.through)
def notify_on_category_add(sender, instance, action, pk_set, **kwargs):
    print(f"DEBUG: Article signal triggered! Action: {action}")
    if action == "post_add":
        for category_id in pk_set:
            category = instance.categories.get(id=category_id)
            print(f"DEBUG: Processing category {category.name}")
            send_post_notification(instance, category)