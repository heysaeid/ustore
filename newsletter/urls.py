from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('confirm/', views.confirm, name='confirm'),
]
