from django.shortcuts import render, get_object_or_404
from book.views import BaseView
from book.models import Book
from .models import Follow, User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import LoginForm

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


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        template_name = 'login/login.html'
        content = {'form': form}
        return render(request, template_name, content)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user.admin)

        if user is not None and not user.admin:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')

        return HttpResponse('You are not User of System')


class LogoutView(LogoutView):
    template_name = 'login/login.html'
    extra_context = {'form': LoginForm()}


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/login'
    template_name = 'login/register.html'
