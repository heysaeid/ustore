from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import (
    home,
    contact,
    product_detail,
    SearchListView,
    TopSellersView,
    RecentlyViewedView,
    TopNewView,
    WishListView,
    ProductListView,
)

class ShopUrlsTest(SimpleTestCase):

    def test_home(self):
        view = resolve(reverse('shop:home'))
        self.assertEqual(
            view.func,
            home,
        )
    
    def test_contact(self):
        view = resolve(reverse('shop:contact'))
        self.assertEqual(
            view.func,
            contact,
        )

    def test_product_detail(self):
        view = resolve(reverse('shop:product_detail', args=['nova7i']))
        self.assertEqual(
            view.func,
            product_detail,
        )

    def test_product_list_view(self):
        view = resolve(reverse('shop:product_list_view', args=['mobile']))
        self.assertEqual(
            view.func.view_class,
            ProductListView,
        )

    def test_search_list_view(self):
        view = resolve(reverse('shop:search_list'))
        self.assertEqual(
            view.func.view_class,
            SearchListView,
        )

    def test_top_sellers_view(self):
        view = resolve(reverse('shop:top_sellers'))
        self.assertEqual(
            view.func.view_class,
            TopSellersView,
        )

    def test_recently_viewed_view(self):
        view = resolve(reverse('shop:recently_viewed'))
        self.assertEqual(
            view.func.view_class,
            RecentlyViewedView,
        )

    def test_top_new_view(self):
        view = resolve(reverse('shop:top_new'))
        self.assertEqual(
            view.func.view_class,
            TopNewView,
        )

    def test_wishlist_view(self):
        view = resolve(reverse('shop:wishlist'))
        self.assertEqual(
            view.func.view_class,
            WishListView,
        )