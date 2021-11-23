from django.test import TestCase
from django.urls import reverse
from coupons.models import Coupon
from datetime import datetime, timedelta

class CouponApplyViewTest(TestCase):

    def setUp(cls):
        now = datetime.now()
        Coupon.objects.create(
            code = 'code50',
            valid_from = now,
            valid_to = now + timedelta(days=10),
            discount = 50,
            active = True,
        )

    def check_redirect(self, response):
        cart_detail_url = reverse('cart:cart_detail')
        self.assertRedirects(response, cart_detail_url)
        new_response = self.client.get(cart_detail_url)
        self.assertContains(new_response, 'Cart Page')

    def test_coupon_apply_GET(self):
        response = self.client.get(reverse('coupons:apply'))
        self.assertEqual(response.status_code, 405)

    def test_coupon_apply_valid_POST(self):
        code = Coupon.objects.get(pk=1)
        response = self.client.post(
            reverse('coupons:apply'),
            {'code':code.code},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('coupon_id'))
        self.check_redirect(response)

    def test_coupon_apply_invalid_POST(self):
        response = self.client.post(
            reverse('coupons:apply'),
            {'code':'code100'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
        self.check_redirect(response)