import json
from decimal import Decimal
import decimal
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory 
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart 
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender


# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=int(cd['quantity']), override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    cahnge_quantity_form = formset_factory(CartAddProductForm)
    cahnge_quantity_form = cahnge_quantity_form(initial=[{'quantity':item['quantity']} for item in cart])
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products, max_results=2)
    return render(request, 'cart/cart_detail.html', {'cart':cart, 'cahnge_quantity_form':cahnge_quantity_form, 'coupon_apply_form':coupon_apply_form, 'recommended_products':recommended_products})

@require_POST
def cart_update(request):
    session = request.session['cart']
    data = {'status':'error'}
    if request.is_ajax():
        data = {'status':'ok'}
        for i, item in enumerate(session):
            quantity = int(request.POST[f'form-{i}-quantity'])
            if quantity > 0 and quantity < 11:
                session[item]['quantity'] = quantity
        request.session.modified = True
    return JsonResponse(data)