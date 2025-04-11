from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    model = Post
    template_name = 'news.html'

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = "post"


def news_list(request):
    news = Post.objects.all().order_by('-created_at')
    return render(request, 'news.html', {'news': news})
# Create your views here.

def news_detail(request, news_id):
    post = Post.objects.get(pk = news_id)
    return render(request, 'news_detail.html', {'post': post})
