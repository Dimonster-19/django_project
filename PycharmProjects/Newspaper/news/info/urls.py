from django.urls import path
from .views import (news_list, news_detail, delete_news, NewsSearch, create_news,
                    edit_news, article_list, create_article, edit_article, delete_article,
                    article_detail, hello,
)
urlpatterns = [
    path('', hello, name='hello'),

    path('news/', news_list, name='news'),

    path('articles/', article_list, name='articles'),

    path('news/<int:news_id>', news_detail, name='news_detail'),

    path('articles/<int:article_id>/', article_detail, name='article_detail'),

    path('news/delete/<int:news_id>/', delete_news, name='delete_news'),

    path('news/search/', NewsSearch.as_view(), name='news_search'),

    path('news/create/', create_news, name='create'),

    path('news/edit/<int:news_id>/', edit_news, name='edit_news'),

    path('articles/add/', create_article, name='create_article'),

    path('articles/edit/<int:article_id>/', edit_article, name='edit_article'),

    path('articles/delete/<int:article_id>/', delete_article, name='delete_article'),
]