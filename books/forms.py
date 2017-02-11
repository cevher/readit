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
