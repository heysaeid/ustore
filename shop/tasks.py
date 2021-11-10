from django.core.mail import send_mail
from django.conf import settings
from celery import task

@task
def contact_send_mail(subject, message, from_email):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [from_email])