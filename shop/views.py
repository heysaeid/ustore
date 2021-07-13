import redis
from django.http import request
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from django.db.models import Count
from django.conf import settings
from django.views.generic import ListView
from .recommender import Recommender
from .models import Category, Product, Slider
from orders.models import OrderItem

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # Top Sellers
    top_sellers_ids = best_selling_products(3)
    top_sellers = Product.objects.filter(id__in=top_sellers_ids)
    # Recently Viewed
    recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
    recenlty_viewed_ids = inOrder(recenlty_viewed_ids, 3)
    recently_viewed = products.filter(id__in=recenlty_viewed_ids).order_by('id')
    # Top new
    top_new = products.filter(id__in=top_new_ids(3))
    sliders = Slider.objects.all()[:4]
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/index.html', {
        'categories': categories, 
        'products': products[:10], 
        'top_sellers': top_sellers, 
        'recently_viewed': recently_viewed, 
        'top_new': top_new,
        'sliders': sliders,
        'cart_product_form':cart_product_form
        }
    )

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    # Save the latest hits
    r.hsetnx('product_visit', product.id, 0)
    r.hincrby('product_visit', product.id)
    r.lpush('recently_viewd', product.id)
    # Products recommender engine
    recommender = Recommender()
    recommended_products = recommender.suggest_products_for([product], 2)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product':product, 'recommended_products':recommended_products, 'cart_product_form':cart_product_form})


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_querset(self):
        qs = super().get_queryset()
        slug = self.kwargs['slug']
        if slug == 'top-sellers':
            products_ids = best_selling_products()
        elif slug == 'recently-viewed':
            recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
            products_ids = inOrder(recenlty_viewed_ids, len(recenlty_viewed_ids))
        elif slug == 'top-new':
            products_ids = top_new_ids()
        else:
            category = get_object_or_404(Category, slug=slug)
            return Product.objects.filter(category=category)
        return qs.filter(id__in=products_ids)

    def get_context_data(self):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        context['page_title'] = self.kwargs['slug'].replace('/', ' ')
        return context


def best_selling_products(num=None):
    top_sellers_count = OrderItem.objects.values('product').annotate(count=Count('product')).order_by()[:num]
    product_ids = [item['product'] for item in top_sellers_count]
    return product_ids

def top_new_ids(num=None):
    list_ids = r.hgetall('product_visit')
    list_ids = sorted(list_ids.items(), key=lambda d: int(d[1]), reverse=True)[:3]
    return [item[0] for item in list_ids]

def inOrder(nums, num):
    nums = map(int, nums)
    ids = []
    for x in nums:
        if x not in ids and len(ids) < num:
            ids.append(x)
    return ids