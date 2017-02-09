from django.db.models import Count
from django.shortcuts import render
from.models import book, Author
from django.views.generic import View, DetailView
# Create your views here.


def list_books(request):
    """
    List the books that have reviews
    """
    books = book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')
    context={
        'books' : books,
    }
    return render(request, "list.html",context)

class AuthorList(View):
    def get(self, request):
        authors = Author.objects.annotate(
        published_books=Count('books')).filter(
        published_books__gt=0)
        context ={
            'authors':authors,
        }
        return render(request, "authors.html", context)

class BookDetail(DetailView):
    model = book
    template_name = 'book.html'

class AuthorDetail(DetailView):
    model=Author
    template_name='author.html'
