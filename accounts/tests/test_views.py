from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import dashboard
from orders.tests.test_models import ProductOrderItemTestMixin


class DashboardViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username = 'testuser',
            password = 'testpass123',
        )
    
    def test_dashboard_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertContains(response, 'Dashboard')

    def test_dashboard_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/accounts/dashboard/' % (reverse('login')))


class OrderDetailViewTest(ProductOrderItemTestMixin, TestCase):

    def test_order_detail_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('order_detail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_detail.html')
        self.assertContains(response, 'Order detail')

    def test_order_detail_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('order_detail', args=['1']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/accounts/order-detail/1/' % (reverse('login')))
        response = self.client.get('%s?next=/accounts/order-detail/1/' % (reverse('login')))
        self.assertContains(response, 'Log In')