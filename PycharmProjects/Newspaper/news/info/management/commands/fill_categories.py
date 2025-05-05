from django.core.management.base import BaseCommand
from info.models import Category


class Command(BaseCommand):
    help = 'Заполняет базу стандартными категориями'

    def handle(self, *args, **options):
        categories = [
            'Наука', 'Технологии', 'Новости',
            'Спорт', 'Искусство'
        ]

        for name in categories:
            Category.objects.get_or_create(name=name)
            self.stdout.write(f'Создана категория: {name}')