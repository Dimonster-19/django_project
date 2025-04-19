from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect

# В mixins.py
class AutoGroupMixin:
    """Миксин для автоматического добавления в группу при регистрации"""
    common_group_name = 'Common'

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            common_group, created = Group.objects.get_or_create(name=self.common_group_name)
            self.object.groups.add(common_group)
            return response
        except Exception as e:
            # Логирование ошибки
            from django.contrib import messages
            messages.error(self.request, f'Ошибка добавления в группу: {e}')
            return super().form_invalid(form)

class GroupRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки принадлежности к группе"""
    group_name = None  # Укажите имя группы в наследнике

    def test_func(self):
        if self.group_name is None:
            raise ValueError("Group name must be specified")
        return self.request.user.groups.filter(name=self.group_name).exists()

    def handle_no_permission(self):
        return redirect('access_denied')  # Создайте это представление