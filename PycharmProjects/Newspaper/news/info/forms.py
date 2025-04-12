from django import forms
from .models import Post, Article

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'pub_date', 'author']

    pub_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date'
            }
        )
    )