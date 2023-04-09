from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_value = self.post_set.aggregate(post_rating=Sum('post_rating'))
        post_rating = 0
        post_rating += post_value.get('post_rating')

        comment_value = self.username.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        comment_rating = 0
        comment_rating += comment_value.get('comment_rating')

        self.author_rating = post_rating * 3 + comment_rating
        self.save()


class Category(models.Model):
    category_title = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'PA'
    news = 'PN'
    POSITION = [
        (article, 'Cтатья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_news = models.CharField(max_length=2, choices=POSITION, default=article)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:123]} ...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
