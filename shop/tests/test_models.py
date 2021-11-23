from django.test import TestCase
from shop.models import Category, Product, Review

class ProductTestMixin(object):

    def setUp(self):
        self.category = Category.objects.create(
            name = 'Mobile',
            slug = 'mobile',
        )

        self.product = Product.objects.create(
            category = self.category,
            name = 'Nova 7i',
            slug = 'nova-7i',
            price = 299.00,
        )


class ProductModelTest(ProductTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        number_of_review = 6
        for num in range(1, number_of_review):
            review = Review.objects.create(
                product = self.product,
                name = f'Lnius {num}',
                email = f'testuser{num}@gmail.com',
                rating = num,
                description = 'great...',
            )

    def test_product_average_score(self):
        average_score = self.product.average_score()
        self.assertEqual(average_score['reviews_count'], 5)
        self.assertEqual(len(average_score['ranges']), 3)
