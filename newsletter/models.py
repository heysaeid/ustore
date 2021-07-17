from django.db import models
from .tasks import newsletter_complete

# Create your models here.
class Subscribe(models.Model):
    email = models.EmailField(unique=True)
    confirm_num = models.CharField(max_length=16)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.subject

    def send(self, request):
        newsletter_complete.delay(self.subject, self.message)