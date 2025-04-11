import re
from django import template

register = template.Library()

# Список нежелательных сочетаний букв
BAD_PATTERNS = [
    r'бля',        # Простой пример
    r'сука',
    r'еба',
    r'муда',
    r'шлю',
    r'пизда',
    r'пизд',
    r'хуй',
    r'аху'
]

@register.filter(name='censor')
def censor(value):
    """
    Фильтр для цензуры нежелательных сочетаний букв.
    """
    for pattern in BAD_PATTERNS:
        regex_pattern = re.compile(pattern, re.IGNORECASE)  # Игнорирование регистра
        value = regex_pattern.sub(lambda x: '*' * len(x.group()), value)
    return value
