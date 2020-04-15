from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import LoginForm


# Create your views here.
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
        if user is not None:
            login(request, user)
            print(request.POST)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')

        return HttpResponse('Sai doiiiiiiiiiiii')
