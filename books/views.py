from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from .models import book, Author
from django.views.generic import View, DetailView
from .forms import ReviewForm,BookForm
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


class ReviewList(View):
    def get(self,request):

    	books = book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

    	context = {
    		'books': books,
            'form': BookForm
    	}

    	return render(request, "list-to-review.html", context)

    def post(self,request):
        form= BookForm(request.POST)
        books= book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
        if form.is_valid():
            form.save()
            return redirect('review-books')
        context ={
            'form': form,
            'books':books
        }
        return render(request, "list-to-review.html", context)



def review_book(request, pk):
    Book = get_object_or_404(book, pk=pk)
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Book.is_favorite = form.cleaned_data['is_favorite']
            Book.review = form.cleaned_data['review']
            Book.save()

            return redirect('review-books')
    else:

        form = ReviewForm
        context = {
            'book': Book,
            'form': form,
        	}
        return render(request,"review-book.html", context)
