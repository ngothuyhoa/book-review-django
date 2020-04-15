from django.urls import path
from .views import BookListView, SearchListView, BookDetailView, BookListByCategoryView
from . import views

app_name = 'book'
urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('category/<int:pk>', BookListByCategoryView.as_view(), name='category'),
    path('search', SearchListView.as_view(), name='search'),
    path('detail/<int:pk>', BookDetailView.as_view(), name='detail'),
]
