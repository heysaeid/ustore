from django.test import TestCase
from django.urls import reverse
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm
from .test_models import ProductOrderItemTestMixin

class OrderCreateViewTest(ProductOrderItemTestMixin, TestCase):
    form_data = {
        'first_name': 'Linus',
        'last_name':'Rogga',
        'address':'PK10',
        'city':'Tehran',
        'county':'Tehran',
        'postal_code':'23412332', 
        'phone':'09300000000',
    }

    def test_order_create_no_cart_GET(self):
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_order_create_GET(self):
        self.client.post(reverse('cart:cart_add', args=['1']), {'quantity':1})
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/create.html'),
        self.assertContains(response, 'Shopping Cart')
        self.failUnless(response.context['form'], OrderCreateForm)

    def test_order_create_for_logged_out_user_POST(self):
        for i in range(1, 4):  
            self.client.post(reverse('cart:cart_add', args=[str(i)]), {'quantity':1})
        response = self.client.post(reverse('orders:order_create'), self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:request'))

    def test_order_create_for_logged_in_user_POST(self):
        self.client.login(username='testuser', password='testpass123')
        for i in range(1, 4):  
            self.client.post(reverse('cart:cart_add', args=[str(i)]), {'quantity':1})
        self.form_data['email'] = 'testuser33@gmail.com'
        self.form_data['password'] = 'testpass123'
        response = self.client.post(reverse('orders:order_create'), self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:request'))