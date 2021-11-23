from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orders.views import (
    OrderCreateView,
    admin_order_detail,
    admin_order_pdf,
)

class OrdersUrlsTest(SimpleTestCase):

    def test_order_create(self):
        view = resolve(reverse('orders:order_create'))
        self.assertEqual(
            view.func.view_class,
            OrderCreateView,
        )

    def test_admin_order_detail(self):
        view = resolve(reverse('orders:admin_order_detail', args=['1']))
        self.assertEqual(
            view.func,
            admin_order_detail,
        )

    def test_admin_order_pdf(self):
        view = resolve(reverse('orders:admin_order_pdf', args=['1']))
        self.assertEqual(
            view.func,
            admin_order_pdf,
        )