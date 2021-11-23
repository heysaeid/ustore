from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Product, Category
from orders.models import Order, OrderItem

class ProductOrderItemTestMixin(object):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username = 'testuser',
            email = 'testuser@gmail.com',
            password = 'testpass123',
        )

        self.category = Category.objects.create(
            name = 'Mobile',
            slug = 'mobile',
        )

        number_of_product = 11
        products = []
        for i in range(1, number_of_product):
            product = Product.objects.create(
                category = self.category,
                name = f'Nova 7i {i}',
                slug = f'nova-7i-{i}',
                price = 299.00,
            )
            if i < 4:
                products.append(product)

        order = Order.objects.create(
            user = user,
            first_name = 'Linus',
            last_name = 'Rogga',
            email = user.email,
            phone = '09300000000',
            address = 'P10',
            city = 'Tehran',
            county = 'Tehran',
            postal_code = '2341234523',
        )

        for product in products:
            order_item = OrderItem.objects.create(
                order = order,
                product = product,
                price = 30.00,
                quantity = 3,
            )

class OrderModelTest(ProductOrderItemTestMixin, TestCase):

    def test_order_get_total_cost(self):
        order = Order.objects.get(pk=1)
        self.assertEqual(order.get_total_cost(), 270)

    
class OrderItemModelTest(ProductOrderItemTestMixin, TestCase):

    def test_order_item_get_cost(self):
        order_item = OrderItem.objects.get(pk=1)
        self.assertEqual(order_item.get_cost(), 90)