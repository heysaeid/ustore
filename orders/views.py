from django.contrib.auth import authenticate, login as auth_login
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin, View
import weasyprint
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Product
from .task import order_created
from shop.recommender import Recommender
from accounts.forms import LoginForm, UserRegistrationForm

# Create your views here.
class OrderCreateView(TemplateResponseMixin, View):
    template_name = 'orders/order/create.html'
    cart = None
    login_form = None
    error_message = None

    def get_form(instance=None, data=None):
        return OrderCreateForm(instance=instance, data=data)

    def dispatch(self, request):
        self.cart = Cart(request)
        self.login_form = LoginForm()
        return super().dispatch(request)

    def get(self, request, *args, **kwargs):
        if self.cart:
            cart_products = [item['product'] for item in self.cart]
            if request.user.is_authenticated:
                form = OrderCreateForm(instance=request.user.orders.first(), request=request)
            else:
                form = OrderCreateForm(request=request)
            return self.render_to_response({'cart':self.cart, 'form':form, 'login_form':self.login_form, 'error_message':self.error_message})
        else:
            return redirect('cart:cart_detail')

    def post(self, request, *args, **kwargs):
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save(commit=False)

            # If the user did not log in, we will create an account
            if not request.user.is_authenticated:
                cd = form.cleaned_data
                ind = cd['email'].index('@')
                username = cd['email'][0:ind]
                data = {'username':username, 'email':cd['email'], 'password1':cd['password'], 'password2':cd['password']}
                register_form = UserRegistrationForm(data)
                if register_form.is_valid():
                    user = register_form.save()
                    auth_user = authenticate(username=user.email, password=cd['password'])
                    auth_login(request, auth_user)
                    order.user = user
                else:
                    self.error_message = register_form
                    return self.render_to_response({'cart':self.cart, 'form':form, 'login_form':self.login_form, 'error_message':self.error_message})      
            else:
                order.user = request.user
            order.final_price = int(self.cart.get_total_price_after_discount()) * 23000
            order.save()
            for item in self.cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            self.cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:request')) 
        return self.render_to_response({'cart':self.cart, 'form':form, 'login_form':self.login_form, 'error_message':self.error_message})      


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response