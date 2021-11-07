from celery import task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@task
def order_created(order_id, first_name, email):
    subject =  f'Order nr. {order_id}'
    message = f'Dear {first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order_id}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return 'order_created_task_done'