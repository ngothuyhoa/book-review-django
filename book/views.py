from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Book, Category, Review, Mark, Favorite, Buy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm, CommentForm, BuyForm
import random
from user.models import User
from django.template import RequestContext, loader
from django.db.models import Count


# Create your views here.
class BaseView(LoginRequiredMixin, ListView):
    login_url = '/login'
    queryset = ''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # random book
        # use flat=True to return a QuerySet of single values instead of 1-tuples:
        id_list = Book.objects.values_list('id', flat=True)
        random_id_list = random.sample(list(id_list), min(len(id_list), 3))
        context['book_random'] = Book.objects.filter(id__in=random_id_list)

        #user random
        id_user_list = list(User.objects.filter(admin=0).values_list('id', flat=True))
        id_user_list.remove(self.request.user.id)
        random_id_user_list = random.sample(id_user_list, min(len(id_user_list), 3))
        context['user_random'] = User.objects.filter(id__in=random_id_user_list)
        context['following_list'] = self.request.user.following.all()

        return context


class IndexView(BaseView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newBooks'] = Book.objects.all().order_by('-id')[:4]
        context['books'] = Book.objects.all()[:4]
        context['favorite_books'] = Book.objects.annotate(num_books=Count('favorites')).order_by('-num_books')[:4]

        return context


class BaseListBookView(BaseView):
    template_name = "home/books/list-book.html"


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
        favorite = book.favorites.all().filter(user=request.user).first()
        id_list = Book.objects.values_list('id', flat=True)
        # book random
        random_id_list = random.sample(list(id_list), min(len(id_list), 3))
        book_random = Book.objects.filter(id__in=random_id_list)
        # user random
        id_user_list = list(User.objects.values_list('id', flat=True))
        id_user_list.remove(self.request.user.id)
        random_id_user_list = random.sample(id_user_list, min(len(id_user_list), 3))
        user_random = User.objects.filter(id__in=random_id_user_list)

        if mark is None:
            mark = {}
            mark['id'] = 0

        content = {
            'book': book,
            'form': ReviewForm(),
            'categories': categories,
            'replyForm': CommentForm(),
            'mark': mark,
            'favorite': favorite,
            'book_random': book_random,
            'user_random': user_random
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
            else:
                idBook = request.POST['read']
                book = get_object_or_404(Book, pk=idBook)
                status = 2
            mark = Mark(
                status=status,
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
            else:
                mark.status = 0
            mark.save(update_fields=['status'])
        return HttpResponseRedirect(request.POST['current'])

class FavoriteBook(DetailBookView):
    def post(self, request, pk):
        if 'favorite' in request.POST:
            book = get_object_or_404(Book, pk=pk)
            favorite = Favorite(
                favorite=1,
                book=book,
                user=request.user
            )
            favorite.save()
        else:
            favorite = Favorite.objects.get(pk=pk)
            favorite.delete()
        return HttpResponseRedirect(request.POST['current'])

class BuyBookView(BaseListBookView):
    template_name = 'home/books/buy-book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        context['book'] = book
        buy = Buy.objects.filter(book=book, user=self.request.user, status=0).last()
        if buy:
            context['form'] = BuyForm(instance=buy)
            context['can_update'] = True
            context['buy'] = buy
        else:
            context['form'] = BuyForm()
            context['can_update'] = False

        return context

    def post(self, request, pk):
        if 'update' in request.POST:
            buy = Buy.objects.get(pk=pk)
            form = BuyForm(request.POST, book=buy.book, user=buy.user, instance=buy)
        else:
            book = get_object_or_404(Book, pk=pk)
            form = BuyForm(request.POST, book=book, user=request.user)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(request.path)

class HistoryBuy(BaseListBookView):
    template_name = 'home/books/buy-book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy = get_object_or_404(Buy, pk=self.kwargs['pk'])
        book = get_object_or_404(Book, pk=buy.book.id)
        context['book'] = book

        if buy:
            context['history'] = True
            context['buy'] = buy
            context['form'] = BuyForm(instance=buy)

        return context




def buyBook(request):
    template = 'admin/buy-book.html'
    buy = Buy.objects.filter(status=0)
    context = {'buy': buy}
    return render(request, template, context)