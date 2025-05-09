import os
from celery import Celery
from celery.schedules import crontab

# 1. Установка переменной окружения Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")

# 2. Создание экземпляра Celery
app = Celery("news")

# 3. Загрузка настроек из settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# 4. Настройка периодических задач
app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'newsletter.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Понедельник 8:00
    },
}

# 5. Дополнительные настройки
app.conf.update(
    timezone='Europe/Moscow',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    worker_prefetch_multiplier=4,
)

# 6. Автоматическое обнаружение задач
app.autodiscover_tasks()

# 7. Тестовая задача (должна быть определена ПОСЛЕ создания app)
@app.task(bind=True, name="celery.debug_task")
def debug_task(self):
    """Улучшенная тестовая задача"""
    import socket
    from datetime import datetime

    info = {
        "status": "success",
        "worker": socket.gethostname(),
        "timestamp": str(datetime.now()),
        "message": "Celery работает корректно!"
    }
    print(f"[CELERY DEBUG] {info}")
    return info