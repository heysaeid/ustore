from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.urls.base import resolve
from shop.tests.test_models import ProductTestMixin
from coupons.forms import CouponApplyForm

# class CreateCartSessionTestMixin(object):
#     
#     def create_cart_session(self):
#         session = self.client.session
#         session['cart'] = {}
#         session['cart']['1'] = {'quantity': 2, 'price':39.00}
#         session.save()


class CartAddViewTest(ProductTestMixin, TestCase):
    
    def test_cart_add_GET(self):
        response = self.client.get(reverse('cart:cart_add', args=['1']))
        self.assertEqual(response.status_code, 405)

    def test_cart_add_POST(self):
        response = self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.client.session.get('cart')), 1)
        cart_detail_url = reverse('cart:cart_detail')
        self.assertRedirects(response, cart_detail_url)
        response = self.client.get(cart_detail_url)
        self.assertContains(response, 'Cart Page')

    def test_cart_add_update_quantity(self):
        self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        response = self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('cart')['1']['quantity'], 2)


class CartRemoveViewTest(ProductTestMixin, TestCase):

    def test_cart_remove_GET(self):
        response = self.client.get(reverse('cart:cart_remove', args=['1']))
        self.assertEqual(response.status_code, 405)

    def test_cart_remove_POST(self):
        self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        response = response = self.client.post(reverse('cart:cart_remove', args=['1']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.client.session.get('cart')), 0)
        cart_detail_url = reverse('cart:cart_detail')
        self.assertRedirects(response, cart_detail_url)
        response = self.client.get(cart_detail_url)
        self.assertContains(response, 'Cart Page')


class CartDetailViewTest(ProductTestMixin, TestCase):
        
    def test_cart_detail_with_product(self):
        self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cart']), 1)
        self.assertEqual(len(response.context['cahnge_quantity_form']), 2)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
        self.assertContains(response, 'Cart Page')
        self.failUnless(response.context['coupon_apply_form'], CouponApplyForm)
        
    def test_cart_detail_no_product(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cart']), 0)
        self.assertEqual(len(response.context['cahnge_quantity_form']), 1)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
        self.assertContains(response, 'Your cart is empty')
        

class CartUpdateViewTest(ProductTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})

    def test_cart_update_GET(self):
        response = self.client.get(reverse('cart:cart_update'))
        self.assertEqual(response.status_code, 405)

    def test_cart_update_POST(self):
        response = self.client.post(reverse('cart:cart_update'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status':'error'}
        )

    def test_cart_update_AJAX(self):
        response = self.client.post(
            reverse('cart:cart_update'),
            {'form-0-quantity':'3'},
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'} 
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('cart')['1']['quantity'], 3)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), 
            {'status': 'ok'},
        )
