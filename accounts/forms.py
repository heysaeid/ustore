from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as AuthenticationAuthForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {'username':{'unique':'A user with that email already exists.'}}


class AuthenticationForm(AuthenticationAuthForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-text', 'autofocus': True}))
    error_messages = {
        'invalid_login': "Please enter a correct email and password. Note that both fields may be case-sensitive."
    }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-text', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}))