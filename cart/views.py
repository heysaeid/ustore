from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart 
from coupons.forms import CouponApplyForm

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
    random_products = Product.objects.order_by('?')[:2]
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', {'cart':cart, 'random_products':random_products, 'coupon_apply_form':coupon_apply_form})