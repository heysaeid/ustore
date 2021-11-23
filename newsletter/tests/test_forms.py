from django.test import TestCase
from newsletter.forms import NewSubscriberForm

class NewSubscriberFormTest(TestCase):

    def test_valid_form(self):
        data = {'email':'testuser@gmail.com'}
        form = NewSubscriberForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = NewSubscriberForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)