from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-text'}))