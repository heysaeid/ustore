from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as login_auth
from .forms import LoginForm

# Create your views here.
def user_login(request):
    message_error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login_auth(request, user)
                return redirect('orders:order_create')
            else:
                message_error = 'Invalid username or password'
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form, 'message_error':message_error})
