from django.http import response
from django.test import TestCase
from django.urls import reverse
from newsletter.models import Subscribe
from newsletter.views import random_digits

class NewViewTest(TestCase):

    def test_new_GET(self):
        response = self.client.get(reverse('newsletter:new'))
        self.assertEqual(response.status_code, 405)

    def test_new_POST(self):
        response = self.client.post(reverse('newsletter:new'))
        self.assertEqual(response.status_code, 200)

    def test_new_AJAX(self):
        response = self.client.post(
            reverse('newsletter:new'),
            {'email':'testuser@gmail.com'},
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status':'ok'}
        )


class ConfirmViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Subscribe.objects.create(
           email = 'testuser@gmail.com',
           confirm_num =  random_digits(),
        )

    def test_confirm_valid_data(self):
        sub = Subscribe.objects.get(pk=1)
        response = self.client.get(
            f'{reverse("newsletter:confirm")}?conf_num={sub.confirm_num}&email={sub.email}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsletter/confirm.html')
        self.assertContains(response, 'Your newsletter subscription was successful')
    
    def test_confirm_invalid_data(self):
        response = self.client.get(
            f'{reverse("newsletter:confirm")}?conf_num=50607081&email=testuser10@gmail.com'
        )
        self.assertEqual(response.status_code, 404)