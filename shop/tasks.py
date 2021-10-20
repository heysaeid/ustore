from django.core.mail import send_mail
from celery import task

@task
def contact_send_mail(subject, message, from_email):
    send_mail(subject, message, 'admin@gmail.com',[from_email])