from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payment.views import (
    send_request,
    verify,
    payment_done,
    payment_canceled,
)

class PaymentUrlsTest(SimpleTestCase):

    def test_send_request(self):
        view = resolve(reverse('payment:request'))
        self.assertEqual(
            view.func,
            send_request,
        )

    def test_verify(self):
        view = resolve(reverse('payment:verify'))
        self.assertEqual(
            view.func,
            verify,
        )

    def test_payment_done(self):
        view = resolve(reverse('payment:done'))
        self.assertEqual(
            view.func,
            payment_done,
        )

    def test_payment_canceled(self):
        view = resolve(reverse('payment:canceled'))
        self.assertEqual(
            view.func,
            payment_canceled,
        )