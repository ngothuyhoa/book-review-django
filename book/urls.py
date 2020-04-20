from django.urls import path
from .views import BookListView, SearchListView, CommentBook, BookListByCategoryView, ReviewBook, MarkBook
from . import views

app_name = 'book'
urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('category/<int:pk>', BookListByCategoryView.as_view(), name='category'),
    path('search', SearchListView.as_view(), name='search'),
    path('review/<int:pk>', ReviewBook.as_view(), name='review'),
    path('comment/<int:pk>', CommentBook.as_view(), name='comment'),
    path('mark/<int:pk>', MarkBook.as_view(), name='mark-book'),
]
