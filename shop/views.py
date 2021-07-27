import redis
from django.http.response import Http404, JsonResponse
from django.core.cache import cache
from django.db.models import Q
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.conf import settings
from django.views.generic import ListView
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .models import Category, Product, Slider
from orders.models import OrderItem
from .forms import ReviewForm, ContactForm

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

# Create your views here.
def home(request):
    # categories = Category.objects.all()
    if 'products' in cache:
        products = cache.get('products')
    else:
        products = Product.objects.filter(available=True)
        cache.set('products', products, timeout=settings.TIMEOUT_PRODUCTS)
    # Top Sellers
    top_sellers_ids = best_selling_products(3)
    top_sellers = products.filter(id__in=top_sellers_ids)
    # Recently Viewed
    recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
    recenlty_viewed_ids = inOrder(recenlty_viewed_ids, 3)
    recently_viewed = products.filter(id__in=recenlty_viewed_ids).order_by('id')
    # Top new
    top_new = products.filter(id__in=top_new_ids(3))
    if 'sliders' in cache:
        sliders = cache.get('sliders')
    else:
        sliders = Slider.objects.all()[:4]
        cache.set('sliders', sliders, timeout=settings.TIMEOUT_SLIDERS)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/index.html', {
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
    review_form = ReviewForm(request.POST or None)
    data = {}
    if request.is_ajax():
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.product = product
            form.save()
            data['id'] = product.id
            data['status'] = 'ok'
        else:
            data['error'] = next(iter(review_form.errors.items()))[1][0]
        return JsonResponse(data)
    # Save the latest hits
    r.hsetnx('product_visit', product.id, 0)
    r.hincrby('product_visit', product.id)
    r.lpush('recently_viewd', product.id)
    # Products recommender engine
    recommender = Recommender()
    recommended_products = recommender.suggest_products_for([product], 2)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product':product,'form':review_form ,'recommended_products':recommended_products, 'cart_product_form':cart_product_form})

def contact(request):
    message= None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                message = 'Email sent successfully, we will reply soon'
                send_mail(cd['subject'], cd['message'], cd['from_email'], ['yozellon@gmail.com'])
            except BadHeaderError:
                message = 'Invaild header found.'
    else:
        form = ContactForm()
    return render(request, 'other/contact.html', {'form':form, 'message':message})

class ProductListMixin(object):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        if self.kwargs.get('slug') == None:
            context['page_title'] = f'search for {self.request.GET.get("s", "")}'
        else:
            context['page_title'] = self.kwargs['slug'].replace('/', ' ')
        return context

class SearchListView(ProductListMixin, ListView):
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('s')
        if query is not None:
            products = Product.objects.filter(Q(name__icontains=query))
        else:
            return Http404
        return products

class ProductListView(ProductListMixin, ListView):

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs['slug']
        if slug == 'top-sellers':
            products_ids = best_selling_products()
        elif slug == 'recently-viewed':
            recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
            products_ids = inOrder(recenlty_viewed_ids, len(recenlty_viewed_ids))
        elif slug == 'top-new':
            products_ids = top_new_ids()
        elif slug == 'wishlist':
            cookie = self.request.COOKIES.get('wishlist')
            products_ids = [int(item) for item in cookie] if cookie  else []
        else:
            category = get_object_or_404(Category, slug=slug)
            if 'product_list_view' in cache:
                products = cache.get("product_list_view")
            else:
                products = Product.objects.filter(category=category)
                cache.set('product_list_view', products, timeout=settings.TIMEOUT_PRODUCT_LIST_VIEW)
            return products
        return qs.filter(id__in=products_ids)


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