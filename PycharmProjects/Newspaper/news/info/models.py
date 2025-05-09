from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    rating = models.IntegerField(default=0)

    @property
    def total_publications(self):
        """Все публикации: статьи из Post и Article"""
        return self.user.posts.count() + self.user.articles.count()

    @property
    def news_count(self):
        """Только новости (Post с type=NEWS)"""
        return self.user.posts.filter(type=Post.NEWS).count()

    @property
    def articles_count(self):
        """Статьи из обеих моделей"""
        return self.user.articles.count() + self.user.posts.filter(type=Post.ARTICLE).count()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NEWS)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return self.title

    @property
    def is_article(self):
        return self.type == self.ARTICLE

    def get_author_name(self):
        return str(self.author)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_posts')

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles', verbose_name="Категории")

    class Meta:
        permissions = [
            ('can_create_article', 'Может создавать статью'),
            ('can_edit_article', 'Может редактировать статью'),
            ('can_delete_article', 'Может удалять статью'),
        ]

    def __str__(self):
        return self.title

    @property
    def is_article(self):
        return True

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', args=[str(self.id)])

    def get_author_name(self):
        return self.author.get_full_name() or self.author.username

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
