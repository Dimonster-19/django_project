from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Article
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Article.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    """
    Отправляет уведомления при связывании статьи с категориями
    """
    # Работаем только при добавлении связей (не при удалении)
    if action != "post_add":
        return

    for category in instance.categories.all():
        subscribers = category.subscribers.exclude(id=instance.author.id)
        logger.info(f"📢 Категория '{category.name}': {subscribers.count()} подписчиков")

        for user in subscribers:
            logger.info(f"✉️ Отправка письма для: {user.email}")
            send_notification(user, instance, category)


def send_notification(user, article, category):
    """Функция отправки email (оставляем без изменений)"""
    subject = f'Новая статья в категории "{category.name}"'
    html_message = render_to_string('account/email/new_article_notification.html', {
        'user': user,
        'article': article,
        'category': category,
        'domain': settings.DOMAIN
    })

    send_mail(
        subject=subject,
        message='',
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )