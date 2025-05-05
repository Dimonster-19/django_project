from django.urls import path
from . import views
from .views import become_author, RulesView

urlpatterns = [
    # Убраны все пути аутентификации (их предоставляет allauth)

    # Личный кабинет
    path('profile/', views.profile, name='profile'),

    # Функционал автора
    path('become-author/', become_author, name='become_author'),

    # Правила
    path('rules/', RulesView.as_view(), name='rules'),
]