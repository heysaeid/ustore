from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart 
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

# Create your views here.
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=int(cd['quantity']), override_quantity=cd['override'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products, max_results=2)
    return render(request, 'cart/cart_detail.html', {'cart':cart, 'recommended_products':recommended_products, 'coupon_apply_form':coupon_apply_form})