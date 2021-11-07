from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView as LoginAuthView
from django.views.generic.edit import CreateView
from orders.models import Order, OrderItem
from .forms import UserRegistrationForm, AuthenticationForm

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

class LoginView(LoginAuthView):
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).select_related('user')
    return render(request, 'accounts/dashboard.html', {'orders':orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, user=request.user, pk=pk)
    return render(request, 'accounts/order_detail.html', {'order':order})