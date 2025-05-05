from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .mixins import AutoGroupMixin
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, BecomeAuthorForm


@login_required
def profile(request):
    is_author = request.user.groups.filter(name='Authors').exists()
    return render(request, 'accounts/profile.html', {'is_author': is_author})

@login_required
def become_author(request):
    if request.method == 'POST':
        form = BecomeAuthorForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            authors_group, created = Group.objects.get_or_create(name='Authors')  # Безопасное получение группы
            request.user.groups.add(authors_group)
            return redirect('profile')
    else:
        form = BecomeAuthorForm()

    return render(request, 'accounts/become_author.html', {'form': form})

class RulesView(TemplateView):
    template_name = 'accounts/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rules'] = [
            "Вы умеете писать 'мама', 'папа' и 'гидронасоснотрехфакторная теплоэлектростанция'",
            "Вы дышите",
        ]
        return context






