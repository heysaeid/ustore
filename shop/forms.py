from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['product']

        widgets = {
            'rating': forms.HiddenInput(attrs={'min':1, 'max':5}),
            'description': forms.Textarea(attrs={'id':'', 'cols':30, 'rows':30}),
        }