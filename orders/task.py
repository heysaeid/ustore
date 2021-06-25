from celery.decorators import task
from django.core.mail import message, send_mail
from .models import Order

@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(pk=order_id)
    subject =  f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    sent_mail = send_mail(subject, message, 'admin@ustore.com', [order.email])
    return sent_mail