from django.shortcuts import render, get_object_or_404
from base.views import BaseView
from book.models import Book
from user.models import Follow, User
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
class ProfileUserView(BaseView):
    template_name = "user/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        id_favorite_books = user.user_favorites.all().values_list('book', flat=True)
        id_reading_books = user.user_marks.all().filter(status=1).values_list('book', flat=True)
        id_read_books = user.user_marks.all().filter(status=2).values_list('book', flat=True)

        context['favorite_books'] = Book.objects.filter(id__in=id_favorite_books)
        context['reading_books'] = Book.objects.filter(id__in=id_reading_books)
        context['read_books'] = Book.objects.filter(id__in=id_read_books)
        context['user_sys'] = user

        follow = Follow.objects.filter(follower=self.request.user, following=user)
        if not follow:
            context['is_follow'] = False
        else:
            context['is_follow'] = True
        return context


class FollowUserView(BaseView):
    def post(self, request, pk):
        if 'follow' in request.POST:
            following = get_object_or_404(User, pk=pk)
            follow = Follow(
                follower=request.user,
                following=following,
            )
            follow.save()
        else:
            follow = Follow.objects.filter(follower=self.request.user, following=pk)
            follow.delete()

        return HttpResponseRedirect(request.POST['current'])
