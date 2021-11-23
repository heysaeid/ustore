from django.test import SimpleTestCase
from cart.forms import CartAddProductForm

class CartAddProductFormTest(SimpleTestCase):

    def test_valid_form(self):
        data = {'quantity':1, 'override':True}
        form = CartAddProductForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CartAddProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)