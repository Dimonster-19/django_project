from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .mixins import AutoGroupMixin
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, BecomeAuthorForm




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя без коммита в БД
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()  # Теперь пользователь сохранен в БД

            common_group, created = Group.objects.get_or_create(name='Common')
            user.groups.add(common_group)

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def profile(request):
    is_author = request.user.groups.filter(name='Authors').exists()
    return render(request, 'accounts/profile.html', {'is_author': is_author})

@login_required
def profile(request):
    is_author = request.user.groups.filter(name='Authors').exists()
    return render(request, 'accounts/profile.html', {'is_author': is_author})

@login_required
def become_author(request):
    if request.method == 'POST':
        form = BecomeAuthorForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            authors_group = Group.objects.get(name='Authors')
            request.user.groups.add(authors_group)
            return redirect('profile')
    else:
        form = BecomeAuthorForm()

    return render(request, 'accounts/become_author.html', {'form': form})





class RulesView(TemplateView):
    template_name = 'accounts/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем правила в контекст
        context['rules'] = [
            " Вы умеете писать 'мама', 'папа' и 'гидронасоснотрехфакторная теплоэлектростанция'",
            " Вы дышите",
            " Все публикуемые материалы должны быть оригинальными и не нарушать авторские права",
            " Запрещено размещение контента, нарушающего законодательство РФ",
            " Автор несет ответственность за достоверность публикуемой информации",
            " Администрация оставляет за собой право модерировать и удалять материалы без объяснения причин",
            " Запрещена реклама и спам в любом виде",
            " При нарушении правил аккаунт автора может быть заблокирован"
        ]
        return context







