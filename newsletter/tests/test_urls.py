from django.test import SimpleTestCase
from django.urls import reverse, resolve
from newsletter.views import new, confirm

class NewsletterUrlsTest(SimpleTestCase):

    def test_new(self):
        view = resolve(reverse('newsletter:new'))
        self.assertEqual(
            view.func,
            new,
        )

    def test_confirm(self):
        view = resolve(reverse('newsletter:confirm'))
        self.assertEqual(
            view.func,
            confirm,
        )