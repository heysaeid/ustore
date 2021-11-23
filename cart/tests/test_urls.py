from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import (
    cart_detail,
    cart_add,
    cart_remove,
    cart_update,
)

class CartUrlsTest(SimpleTestCase):

    def test_cart_detail(self):
        view = resolve(reverse('cart:cart_detail'))
        self.assertEqual(
            view.func,
            cart_detail,
        )

    def test_cart_update(self):
        view = resolve(reverse('cart:cart_update'))
        self.assertEqual(
            view.func,
            cart_update,
        )

    def test_cart_add(self):
        view = resolve(reverse('cart:cart_add', args=['1']))
        self.assertEqual(
            view.func,
            cart_add,
        )

    def test_cart_remove(self):
        view = resolve(reverse('cart:cart_remove', args=['1']))
        self.assertEqual(
            view.func,
            cart_remove,
        )