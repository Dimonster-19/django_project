# tasks.py
from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_notification_task(self, user_email, subject, html_message):
    """
    Фоновая задача для отправки email-уведомления
    """
    try:
        send_mail(
            subject=subject,
            message='',  # Текстовая версия (пустая, так как используем html)
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )
    except Exception as e:
        logger.error(f"Ошибка отправки письма для {user_email}: {str(e)}")
        raise self.retry(exc=e, countdown=60)  # Повторить через 60 сек