from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.http import response
from django.test import TestCase
from django.urls import reverse
from redis import Redis
from orders.tests.test_models import ProductOrderItemTestMixin
from shop.tests.test_models import ProductTestMixin
from cart.forms import CartAddProductForm
from shop.models import Slider
from shop.forms import ReviewForm, ContactForm


class CheckDuplicatesTestMixin(ProductOrderItemTestMixin):

    def check_of_duplicates(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')
        self.assertIsNotNone(response.context['page_title'])
        self.failUnless(response.context['cart_product_form'], CartAddProductForm)

class HomeViewTest(ProductOrderItemTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        image = open(f'{settings.BASE_DIR}/static/img/h4-slide.png', 'br')
        Slider.objects.create(
            title = 'Slider ',
            subtitle = 'slider subtitle',
            image = SimpleUploadedFile(image.name, image.read()),
            url = 'http://example.url',
        )

    def test_home(self):
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertContains(response, 'Home')
        self.failUnless(response.context['cart_product_form'], CartAddProductForm)

    def test_home_recently_viewed(self):
        for i in range(5, 8):
            self.client.get(reverse('shop:product_detail', args=[f'nova-7i-{i}']))
        response = self.client.get(reverse('shop:home'))
        self.assertListEqual(
            [7, 6, 5], 
            [item.id for item in response.context['recently_viewed']]
        )

    def test_home_top_new(self):
        for i in range(5, 8):
            for j in range(0, 5):
                self.client.get(reverse('shop:product_detail', args=[f'nova-7i-{i}']))
        response = self.client.get(reverse('shop:home'))
        self.assertListEqual(
            [5, 6, 7], 
            [item.id for item in response.context['top_new']]
        )

    def test_home_top_sellers(self):
        response = self.client.get(reverse('shop:home'))
        self.assertListEqual(
            [1, 2, 3], 
            [item.id for item in response.context['top_sellers']]
        )
    
    def test_home_slider(self):
        response = self.client.get(reverse('shop:home'))
        self.assertTrue(response.context['sliders'].count())


class ProductDetailViewTest(ProductTestMixin, TestCase):

    def test_product_detail(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/detail.html')
        self.assertContains(response, self.product.name)
        self.failUnless(response.context['cart_product_form'], CartAddProductForm)
        self.failUnless(response.context['form'], ReviewForm)

    def test_product_detail_AJAX(self):
        response = self.client.post(
            self.product.get_absolute_url(),
            {'name': 'Linus', 'email': 'linus@gmail.com', 'rating': 5, 'description': 'great'},
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'id': self.product.id, 'status': 'ok'},
        )


class ContactViewTest(TestCase):

    def test_contact_GET(self):
        response = self.client.get(reverse('shop:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/contact.html')
        self.assertContains(response, 'Contact')
        self.assertIsNone(response.context['message'])
        self.failUnless(response.context['form'], ContactForm)
    
    def test_contact_POST(self):
        response = self.client.post(
            reverse('shop:contact'),
            {'subject':'Work', 'from_email':'linus@gmail.com', 'message':'Hello World'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['message'],
            'Email sent successfully, we will reply soon',
        )


class SearchListViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_search_list_with_value_view(self):
        response = self.client.get('%s?s=nova' % reverse('shop:search_list'))
        self.check_of_duplicates(response)

    def test_search_list_no_value_view(self):
        response = self.client.get(reverse('shop:search_list'))
        self.assertEqual(response.status_code, 404)


class ProductListViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list_view', args=[self.category.slug]))
        self.check_of_duplicates(response)
        self.assertContains(response, self.category.name)


class TopSellersViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_top_sellers_view(self):
        response = self.client.get(reverse('shop:top_sellers'))
        self.check_of_duplicates(response)


class RecentlyViewedViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_recently_viewed_view(self):
        response = self.client.get(reverse('shop:recently_viewed'))
        self.check_of_duplicates(response)


class TopNewViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_top_new_view(self):
        response = self.client.get(reverse('shop:top_new'))
        self.check_of_duplicates(response)


class WishlistViewTest(CheckDuplicatesTestMixin, TestCase):

    def test_wishlist_view(self):
        response = self.client.get(reverse('shop:wishlist'))
        self.check_of_duplicates(response)