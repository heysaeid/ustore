from django.test import SimpleTestCase
from coupons.forms import CouponApplyForm

class CouponApplyFormTest(SimpleTestCase):

    def test_valid_form(self):
        data = {'code':'as21sa1'}
        form = CouponApplyForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CouponApplyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)