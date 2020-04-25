from django.contrib import admin
from .models import Book, Category, Review, Comment, Mark, Favorite, Buy
from django.conf.urls import url
from .views import buyBook
from django.http import HttpResponse
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [
            path('my_view/', self.admin_view(buyBook))
        ]
        return urls

admin_site = MyAdminSite()
# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Mark)
admin.site.register(Favorite)
admin.site.register(Buy)
