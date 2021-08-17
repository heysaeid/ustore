from celery import task
from django.core.mail import send_mail
from . import models

@task
def subscribe_complete(id):
    sub = models.Subscribe.objects.get(id=id)
    subject = 'Newsletter Confirmation'
    message = f'<a href="/newsletter/confirm/?email={sub.email}&conf_num={sub.confirm_num}">clicking here to confirm your registration<</a>'
    send_mail(subject, message, sub.email, ['ustore@info.com'])

@task
def newsletter_complete(subject, message):
    subcribers = models.Subscribe.objects.filter(confirmed=True)
    for sub in subcribers:
        send_mail(subject, message, 'ustore@info.com', [sub.email])