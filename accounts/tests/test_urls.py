from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import dashboard, order_detail

class AccountsUrlsTest(SimpleTestCase):

    def test_dashboard(self):
        view = resolve(reverse('dashboard'))
        self.assertEqual(
            view.func,
            dashboard,
        )

    def test_order_detail(self):
        view = resolve(reverse('order_detail', args=['1']))
        self.assertEqual(
            view.func,
            order_detail,
        )