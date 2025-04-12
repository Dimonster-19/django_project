from django.db import models
from django.contrib.auth.models import User

# Создание пользователей User
user1 = User.objects.create_user('username1', password='password1')
user2 = User.objects.create_user('username2', password='password2')
user3 = User.objects.create_user('username3', password='password3')

#Создание авторов Author
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
author3 = Author.objects.create(user=user3)

# Создание категорий
category1 = Category.objects.create(name='Технологии')
category2 = Category.objects.create(name='Наука')
category3 = Category.objects.create(name='Искусство')
category4 = Category.objects.create(name='Спорт')

# Создание статей article
article7 = Post.objects.create(
    author=author,
    type=Post.ARTICLE,
    title='Человек — единственное млекопитающее, обладающее подбородком',
    content='Среди всех животных единственным млекопитающим с подбородком является человек. '
             'Этот факт выделяет нас среди других представителей класса.',
)
article7.categories.add(category_tech)



# Добавление новости news
news1 = Post.objects.create(
    author=author1,
    type=Post.NEWS,
    title='Первая новость',
    content='Содержание первой новости...',
)
news1.categories.add(category_tech)

# Присваивание дополнительных категорий
category_tech = Category.objects.get(name='Технологии')
category_science = Category.objects.get(name='Наука')
category_art = Category.objects.get(name='Искусство')
category_sport = Category.objects.get(name='Спорт')

article2.categories.add(category_tech, category_art)
article1.categories.add(category_science, category_sport)
news1.categories.add(category_tech, category_art)

# Создание комментариев
comment1 = Comment.objects.create(
    post=article1,
    user=user1,
    content='Отличная статья! Очень понравилась.',
    rating=5,
)

comment2 = Comment.objects.create(
    post=article2,
    user=user2,
    content='Интересный материал, но есть вопросы.',
    rating=4,
)

comment3 = Comment.objects.create(
    post=news1,
    user=user1,
    content='Хорошие новости! Спасибо за обновления.',
    rating=5,
)

comment4 = Comment.objects.create(
    post=news1,
    user=user2,
    content='Это важная информация. Полезно знать!',
    rating=4,
)
# Функции like() и dislike()
article1 = Post.objects.get(title='Первая статья')
article2 = Post.objects.get(title='Вторая статья')
news1 = Post.objects.get(title='Первая новость')
comment1 = Comment.objects.get(content__contains='Отличная статья')
comment2 = Comment.objects.get(content__contains='Интересный материал')
comment3 = Comment.objects.get(content__contains='Хорошие новости')
comment4 = Comment.objects.get(content__contains='Это важная информация')

article1.like()
article2.dislike()
news1.like()
news1.like()

comment1.like()
comment3.dislike()
comment2.like()
comment4.dislike()

# Проверка изменения рейтинга
print(f'Article 1 rating: {article1.rating}')
print(f'Article 2 rating: {article2.rating}')
print(f'News 1 rating: {news1.rating}')

print(f'Comment 1 rating: {comment1.rating}')
print(f'Comment 2 rating: {comment2.rating}')
print(f'Comment 3 rating: {comment3.rating}')
print(f'Comment 4 rating: {comment4.rating}')

# Обновление рейтинга авторов
author1 = Author.objects.get(user__username='username1')
author2 = Author.objects.get(user__username='username2')

author1.update_rating()
author2.update_rating()

print(f"Author1 ({author1.user.username}) rating: {author1.rating}")
print(f"Author2 ({author2.user.username}) rating: {author2.rating}")

# Сортировка авторов по рейтингу
best_author = Author.objects.order_by('-rating').first()

if best_author:
    print(f"Лучший пользователь: {best_author.user.username}, Рейтинг: {best_author.rating}")
else:
    print("Авторы не найдены.")

# Вывод даты добавления, username автора, рейтинга, заголовка и превью лучшей статьи,
# основываясь на лайках/дизлайках к этой статье
best_post = Post.objects.filter(type=Post.ARTICLE).order_by('-rating').first()

if best_post:
    username = best_post.author.user.username
    date_added = best_post.created_at.strftime('%Y-%m-%d %H:%M:%S')
    rating = best_post.rating
    title = best_post.title
    preview = best_post.content[:100]

    print(f"Дата добавления: {date_added}")
    print(f"Автор: {username}")
    print(f"Рейтинг: {rating}")
    print(f"Заголовок: {title}")
    print(f"Превью: {preview}")
else:
    print("Нет доступных статей.")

# Вывести все комментарии к статье
best_post = Post.objects.filter(type=Post.ARTICLE).order_by('-rating').first()

if best_post:
    comments = Comment.objects.filter(post=best_post).order_by('-created_at')  # Сортировка по дате для удобства

    for comment in comments:
        date_added = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Форматируйте дату по необходимости
        username = comment.user.username
        rating = comment.rating
        text = comment.content

        print(f"Дата: {date_added}")
        print(f"Пользователь: {username}")
        print(f"Рейтинг: {rating}")
        print(f"Текст: {text}")
        print("-" * 40)  # Разделитель между комментариями для читаемости
else:
    print("Статья не найдена или нет комментариев.")
