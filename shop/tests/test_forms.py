from django.test import TestCase
from shop.forms import ReviewForm, ContactForm

class ReviewFormTest(TestCase):

    def test_valid_data(self):
        data = {
            'name': 'linus',
            'email': 'linus@gmail.com',
            'rating': 5,
            'description': 'It\'s great'
        }
        form = ReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ReviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class ContactFormTest(TestCase):

    def test_valid_data(self):
        data = {
            'subject': 'Work!',
            'from_email': 'testuser@gmail.com',
            'message': 'Hello World',
        }
        form = ContactForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)