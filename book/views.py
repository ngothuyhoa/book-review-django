from django.shortcuts import render
from django.views.generic import ListView, DetailView
from book.models import Book, Category
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class BaseListBookView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = "home/books/list-book.html"
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookListView(BaseListBookView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()[:4]
        context['title'] = 'All'
        return context


class BookListByCategoryView(BaseListBookView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['books'] = category.book_set.all()
        context['title'] = category.title

        return context


class SearchListView(BaseListBookView):
    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(
            Q(title__icontains=search) | Q(author__icontains=search)
        )
        context['title'] = 'Result search: "' + search + '"'
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'home/books/detail-book.html'
