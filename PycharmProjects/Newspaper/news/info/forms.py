from django import forms
from .models import Post, Article, Category, PostCategory
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User

User = get_user_model()


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        required=True,
        label="Категории"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Введите содержание новости'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Удаляем поле автора при редактировании
        if self.instance and self.instance.pk:
            if 'author' in self.fields:
                del self.fields['author']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.request.user.is_superuser:
            instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ArticleForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        required=True,
        label="Категории"
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'pub_date', 'author', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Содержание статьи'
            }),
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control select2'
            })
        }

class NewsSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Название')
    author = forms.CharField(required=False, label='Автор')
    date_after = forms.DateField(required=False, label='Дата после', widget=forms.DateInput(attrs={'type': 'date'}))
    date_before = forms.DateField(required=False, label='Дата до', widget=forms.DateInput(attrs={'type': 'date'}))


class ArticleFilterForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='Название',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
    )
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Автор',
        empty_label="Все авторы"
    )
    date_after = forms.DateField(
        required=False,
        label='Дата после',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_before = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Категории'
    )