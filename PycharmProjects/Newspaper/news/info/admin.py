# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Post
from .utils import get_user_display


# Расширяем стандартную админку User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


# Регистрируем кастомную админку
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Настройка отображения постов
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_author', 'created_at']

    def display_author(self, obj):
        return get_user_display(obj.author)

    display_author.short_description = 'Автор'