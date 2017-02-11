from django import forms
from .models import book


class ReviewForm(forms.Form):

    is_favorite = forms.BooleanField(
        label= 'Favorite?',
        help_text = 'In your top 100 books of all time',
        required = False
    )

    review = forms.CharField(
        widget = forms.Textarea,
        min_length=300,
        error_messages = {
            'required': 'Please enter your review',
            'min_length': 'Please write at least 300 characters. You have written %(show_value)s'
        }
    )

class BookForm(forms.ModelForm):
    class Meta:
        model= book
        fields=['title', 'authors']
    def clean(self):
        super(BookForm,self).clean()

        try:
            title =self.cleaned_data.get('title')
            authors =self.cleaned_data.get('authors')
            Book= book.objects.get(title=title,authors=authors)

            raise forms.ValidationError(
                'The book{} by {} already exists'.format(title, Book.list_authors()),
                code='bookexists'
            )

        except book.DoesNotExist:
            return self.cleaned_data
