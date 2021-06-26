from django.http import request
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .models import Category, Product

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    template_path = 'shop/index.html'
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        template_path = 'shop/product_list.html'
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, template_path, {'category':category, 'categories':categories, 'products':products, 'cart_product_form':cart_product_form})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 2)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product':product, 'recommended_products':recommended_products, 'cart_product_form':cart_product_form})