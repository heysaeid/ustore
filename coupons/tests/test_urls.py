from django.test import SimpleTestCase
from django.urls import reverse, resolve
from coupons.views import coupon_apply

class CouponsUrlsTest(SimpleTestCase):

    def test_coupon_apply(self):
        view = resolve(reverse('coupons:apply'))
        self.assertEqual(
            view.func,
            coupon_apply,
        )