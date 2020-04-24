from django.shortcuts import render
from django.views import View
from django.views.generic import View, ListView
from book.models import Book, Category
from user.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import random


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
        id_user_list = list(User.objects.values_list('id', flat=True))
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
        return context
