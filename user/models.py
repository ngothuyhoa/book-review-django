from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class User(AbstractUser):
    avatar = models.FileField(upload_to='static/home/images/uploads/avatars/', null=True)
    choice_role = ((0, 'admin'), (1, 'user'))
    role = models.IntegerField(choices=choice_role, default=0)
    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
