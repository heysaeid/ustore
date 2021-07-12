from .cart import Cart
from shop.models import Category

def cart(request):
    return {'cart':Cart(request)}

def categories(request):
    return {'categories': Category.objects.order_by()[:5]}