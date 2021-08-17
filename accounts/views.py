from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic.edit import CreateView
from orders.models import Order, OrderItem
from .forms import UserRegistrationForm, LoginForm
from .decorators import is_login

# Create your views here.
class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password2'])
        auth_login(self.request, user)
        return result

@is_login
def login(request):
    error_message  = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user:
                auth_login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return redirect('shop:home')
            else:
                error_message = 'Invalid username or password'
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form, 'error_message':error_message})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('shop:home'))

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('id')
    return render(request, 'accounts/dashboard.html', {'orders':orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, user=request.user, pk=pk)
    return render(request, 'accounts/order_detail.html', {'order':order})