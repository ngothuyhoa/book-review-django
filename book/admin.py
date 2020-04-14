from django.contrib import admin
from .models import Book, Category, Review, Comment, Mark

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Mark)
