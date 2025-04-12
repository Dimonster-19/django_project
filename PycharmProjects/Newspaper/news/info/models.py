from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # 1. Суммарный рейтинг всех статей автора, умноженный на 3
        post_ratings = self.posts.aggregate(total=models.Sum('rating'))['total'] or 0
        post_ratings_sum = post_ratings * 3

        # 2. Суммарный рейтинг всех комментариев автора
        comment_ratings = self.user.comments.aggregate(total=models.Sum('rating'))['total'] or 0

        # 3. Суммарный рейтинг всех комментариев к статьям автора
        post_comment_ratings = self.posts.aggregate(
            total=models.Sum('comments__rating')
        )['total'] or 0

        # Обновление общего рейтинга автора
        self.rating = post_ratings_sum + comment_ratings + post_comment_ratings
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        # увеличивает рейтинг записи на единицу
        self.rating += 1
        self.save()

    def dislike(self):
        # уменьшает рейтинг записи на единицу
        self.rating -= 1
        self.save()

    def preview(self):
        # Возвращает первые 124 символа текста статьи + многоточие
        return self.content[:124] + '...'

    def __str__(self):
        return self.title

class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_posts')

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        # увеличивает рейтинг записи на единицу
        self.rating += 1
        self.save()

    def dislike(self):
        # уменьшает рейтинг записи на единицу
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title} - {self.content[:20]}"

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    class Meta:
        permissions = [
            ('can_create_article', 'Может создавать статью'),
            ('can_edit_article', 'Может редактировать статью'),
            ('can_delete_article', 'Может удалять статью'),
        ]

    def __str__(self):
        return self.title