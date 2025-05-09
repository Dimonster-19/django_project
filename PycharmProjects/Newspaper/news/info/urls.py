from django.urls import path
from .views import (news_list, news_detail, delete_news, news_search, create_news,
                    edit_news, article_list, create_article, edit_article, delete_article,
                    article_detail, hello, category_news, article_search,
                    subscribe_category, category_articles

)
urlpatterns = [
    path('', hello, name='hello'),

    path('news/', news_list, name='news'),
    path('news/<int:news_id>', news_detail, name='news_detail'),
    path('news/delete/<int:news_id>/', delete_news, name='news_delete'),
    path('news/search/', news_search, name='news_search'),
    path('news/create/', create_news, name='create'),
    path('news/edit/<int:news_id>/', edit_news, name='edit_news'),

    path('category/<str:category_name>/', category_news, name='category_news'),
    path('category/<int:category_id>/subscribe/', subscribe_category, name='subscribe_category'),
    path('articles/category/<str:category_name>/', category_articles, name='category_articles'),

    path('articles/', article_list, name='articles'),
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    path('articles/add/', create_article, name='create_article'),
    path('articles/edit/<int:article_id>/', edit_article, name='edit_article'),
    path('articles/delete/<int:article_id>/', delete_article, name='delete_article'),
    path('article_search/', article_search, name='article_search'),

]