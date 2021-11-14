import redis
from django.http.response import Http404, JsonResponse
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.mail import BadHeaderError
from django.conf import settings
from django.views.generic import ListView
from cart.forms import CartAddProductForm
from .models import Category, Product, Slider
from .forms import ReviewForm, ContactForm
from .tasks import contact_send_mail
from .recommender import Recommender
from .utils import best_selling_products, top_new_ids, inOrder

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

# Create your views here.
def home(request):
    if 'products' in cache:
        products = cache.get('products')
    else:
        products = Product.objects.filter(available=True)
        cache.set('products', products, timeout=settings.TIMEOUT_PRODUCTS)

    # Top Sellers
    top_sellers_ids = best_selling_products(products, 3)
    top_sellers = products.filter(id__in=top_sellers_ids)

    # Recently Viewed
    recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
    recenlty_viewed_ids = inOrder(recenlty_viewed_ids, 3)
    recently_viewed = list(products.filter(id__in=recenlty_viewed_ids))
    recently_viewed.sort(key=lambda x: recenlty_viewed_ids.index(x.id))

    # Top new
    top_new = products.filter(id__in=top_new_ids(r, 3))

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
    # Post a comment
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
                contact_send_mail.delay(cd['subject'], cd['message'], cd['from_email'])
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
    page_title = None

    def get_context_data(self):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        context['page_title'] = self.page_title
        return context


class SearchListView(ProductListMixin, ListView):
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('s')
        if query is not None:
            products = qs.filter(Q(name__icontains=query))
        else:
            raise Http404
        return products

    def get_context_data(self):
        context = super().get_context_data()
        context['page_title'] = f'search for {self.request.GET.get("s", "")}'
        return context
        

class ProductListView(ProductListMixin, ListView):
    category_title = None

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        self.category_title = category.name
        if 'product_list_view' in cache:
            products = cache.get("product_list_view")
        else:
            products = qs.filter(category=category)
            cache.set('product_list_view', products, timeout=settings.TIMEOUT_PRODUCT_LIST_VIEW)
        return products

    def get_context_data(self):
        context = super().get_context_data()
        context['page_title'] = self.category_title
        return context


class TopSellersView(ProductListMixin, ListView):
    page_title = 'Top Sellers'

    def get_queryset(self):
        qs = super().get_queryset()
        products_ids = best_selling_products(qs=qs)
        return qs.filter(id__in=products_ids)


class RecentlyViewedView(ProductListMixin, ListView):
    page_title = 'Recently Viewed'

    def get_queryset(self):
        recenlty_viewed_ids = r.lrange('recently_viewd', 0, -1)
        products_ids = inOrder(recenlty_viewed_ids, len(recenlty_viewed_ids))
        return super().get_queryset().filter(id__in=products_ids)


class TopNewView(ProductListMixin, ListView):
    page_title = 'Top New'

    def get_queryset(self):
        products_ids = top_new_ids(redis=r)
        return super().get_queryset().filter(id__in=products_ids)


class WishListView(ProductListMixin, ListView):
    page_title = 'WishList'

    def get_queryset(self):
            cookie = self.request.COOKIES.get('wishlist')
            products_ids = [int(item) for item in cookie] if cookie  else []
            return super().get_queryset().filter(id__in=products_ids)