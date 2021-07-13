from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as login_auth
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from .forms import LoginForm
from .decorators import is_login

# Create your views here.
@is_login
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

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('id')
    return render(request, 'accounts/dashboard.html', {'orders':orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, user=request.user, pk=pk)
    return render(request, 'accounts/order_detail.html', {'order':order})