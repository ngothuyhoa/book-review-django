from django.shortcuts import render
from django.views.generic import ListView, DetailView
from book.models import Book, Category
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
class BaseListBookView(ListView):
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


# class NewBookListView(BaseListBookView, TemplateView):
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Category.objects.get(pk=1).book_set.all()
#
#         return context


def categoryBook(request, category_id):
    template = 'home/books/list-book.html'
    category = Category.objects.get(pk=category_id)
    books = category.book_set.all()
    categories = Category.objects.all()
    content = {
        'books': books,
        'categories': categories,
        'title': Category.objects.get(pk=category_id).title
    }
    return render(request, template, content)

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


def detailBook(request):
    template =  'home/books/detail-book.html'
    return render(request, template)
