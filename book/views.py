from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from book.models import Book, Category, Review, Mark
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


class DetailBookView(BaseListBookView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        categories = Category.objects.all()
        mark = book.marks.all().filter(user=request.user).first()
        if mark is None:
            mark = {}
            mark['id'] = 0

        content = {
            'book': book,
            'form': ReviewForm(),
            'categories': categories,
            'replyForm': CommentForm(),
            'mark': mark
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


class MarkBook(DetailBookView):
    def post(self, request, pk):
        if pk == 0:
            if 'reading' in request.POST:
                idBook = request.POST['reading']
                book = get_object_or_404(Book, pk=idBook)
                status = 1
                favorite = 0
            elif 'read' in request.POST:
                idBook = request.POST['read']
                book = get_object_or_404(Book, pk=idBook)
                status = 2
                favorite = 0,
            else:
                idBook = request.POST['favorite']
                book = get_object_or_404(Book, pk=idBook)
                status = 0
                favorite = 1,
            mark = Mark(
                status=status,
                favorite=favorite,
                book=book,
                user=request.user
            )
            mark.save()
        else:
            mark = Mark.objects.get(pk=pk)
            if 'reading' in request.POST:
                mark.status = 1
            elif 'read' in request.POST:
                mark.status = 2
            elif 'unread' in request.POST:
                mark.status = 0
            elif 'favorite' in request.POST:
                mark.favorite = 1
            else:
                mark.favorite = 0
            mark.save(update_fields=['status', 'favorite'])
        return HttpResponseRedirect(request.POST['current'])
