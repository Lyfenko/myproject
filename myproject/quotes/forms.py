from django import forms
from .models import Author, Quote


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'bio')


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('author', 'text', 'tags')
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'Enter comma-separated tags'}),
        }


class ScrapeForm(forms.Form):
    url = forms.URLField()
