from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from book.models import Book, Category

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')


class IndexView(ListView):
    template_name = "home/index.html"
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newBooks'] = Book.objects.all().order_by('-id')[:4]
        context['books'] = Book.objects.all()[:4]
        context['categories'] = Category.objects.all()

        return context
