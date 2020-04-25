from django.db import models
from user.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    image = models.FileField(upload_to='static/home/images/uploads/%Y/%m/')
    author = models.CharField(max_length=100)
    pages = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Mark(models.Model):
    choice_status = ((0, 'Unread'), (1, 'Reading'), (2, 'Read'))
    status = models.IntegerField(choices=choice_status, default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='marks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_marks')


class Favorite(models.Model):
    choice_favorite = ((1, 'Favorite'),)
    favorite = models.IntegerField(choices=choice_favorite, default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='user_favorites')


class Buy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='buys')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, default='')
    note = models.TextField(default='')
    choice_status = ((0, 'Default'), (1, 'Approve'), (2, 'Cancel'))
    status = models.IntegerField(choices=choice_status, default=0)
    reated_at = models.DateTimeField(auto_now_add=True)