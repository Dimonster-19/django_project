from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import register, become_author, RulesView

urlpatterns = [
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

    # Личный кабинет
    path('profile/', views.profile, name='profile'),

    # Смена пароля (опционально)
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html'),name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('become-author/', become_author, name='become_author'),

    path('rules/', RulesView.as_view(), name='rules'),

]