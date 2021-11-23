from django.test import TestCase
from orders.forms import OrderCreateForm

class OrderCreateFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'first_name': 'linuse',
            'last_name': 'rogge',
            'address': 'P10',
            'city': 'Tehran',
            'county':'Tehran',
            'postal_code': '2341234523',
            'phone': '989300000000',
            'email': 'linusrogge@gmail.com',
            'password': 'testpass123',
        }
        form = OrderCreateForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = OrderCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)