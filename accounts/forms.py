from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']