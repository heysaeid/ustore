import weasyprint
from django.contrib.auth import authenticate, login as auth_login
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.base import TemplateResponseMixin, View
from accounts.forms import AuthenticationForm, UserRegistrationForm
from cart.cart import Cart
from shop.models import Product
from shop.recommender import Recommender
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created

# Create your views here.
class OrderCreateView(TemplateResponseMixin, View):
    template_name = 'orders/order/create.html'
    cart = None
    login_form = None
    error_message = None
    is_login = False

    def dispatch(self, request):
        self.cart = Cart(request)
        self.is_login = request.user.is_authenticated
        if not self.is_login:
            self.login_form = AuthenticationForm()
        return super().dispatch(request)

    def get(self, request, *args, **kwargs):
        if self.cart:
            cart_products = [item['product'] for item in self.cart]
            r = Recommender()
            r.products_bought(product_ids=[item['product'].id for item in self.cart])
            form = OrderCreateForm(is_login=self.is_login)
            if self.is_login:
                form = OrderCreateForm(instance=request.user.orders.first(), is_login=self.is_login)
            return self.render_to_response({'cart':self.cart, 'form':form, 'login_form':self.login_form, 'error_message':self.error_message})
        return redirect('cart:cart_detail')

    def post(self, request, *args, **kwargs):
        form = OrderCreateForm(request.POST, is_login=self.is_login)
        if form.is_valid():
            order_form = form.save(commit=False)
            if not self.is_login:
                cd = form.cleaned_data
                ind = cd['email'].index('@')
                username = cd['email'][0:ind]
                data = {'username':username, 'email':cd['email'], 'password1':cd['password'], 'password2':cd['password']}
                register_form = UserRegistrationForm(data=data)
                if register_form.is_valid():
                    user = register_form.save()
                    order_form.user = user
                    auth_user = authenticate(username=user.email, password=cd['password'])
                    auth_login(request, auth_user)
                else:
                    self.error_message = register_form
                    return self.render_to_response({'cart':self.cart, 'form':form, 'login_form':self.login_form, 'error_message':self.error_message})      
            else:
                order_form.user = request.user
            order_form.final_price = int(self.cart.get_total_price_after_discount()) * 27000
            order_form.save()
            my_orders = []
            for item in self.cart:
                my_orders.append(OrderItem(order=order_form, product=item['product'], price=item['price'], quantity=item['quantity']))
            OrderItem.objects.bulk_create(my_orders)
            self.cart.clear()
            # launch asynchronous task
            order_created.delay(order_form.id, order_form.first_name, order_form.email)
            request.session['order_id'] = order_form.id
            r = Recommender
            r.products_bought([item['product'].id for item in self.cart])
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
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS('http://127.0.0.1:8000/static/css/pdf.css')])
    return response