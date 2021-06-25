from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]