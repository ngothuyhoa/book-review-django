from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from book.models import Book, Category, Review
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from book.forms import ReviewForm, CommentForm


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
        context['books'] = Book.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = 'CommentForm'

        return context


class DetailBookView(BaseListBookView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        categories = Category.objects.all()
        content = {
            'book': book,
            'form': ReviewForm(),
            'categories': categories,
            'replyForm': CommentForm()
        }
        return render(request, 'home/books/detail-book.html', content)


class ReviewBook(DetailBookView):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = ReviewForm(request.POST, book=book, user=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)


class CommentBook(DetailBookView):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = CommentForm(request.POST, review=review, user=request.user)

        if form.is_valid():
            form.save()
            print(request.POST)
            return HttpResponseRedirect(request.POST['current'])
        else:
            return HttpResponse('not saved yet')
