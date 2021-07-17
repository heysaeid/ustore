from django import forms
from django.forms import widgets
from .models import Subscribe

class NewSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

        widgets = {
            'email':forms.EmailInput(attrs={'placeholder':'Type your email'})
        }