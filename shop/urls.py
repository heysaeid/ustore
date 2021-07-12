from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/top-seleres/', views.top_sellers, name='top_sellers'),
    path('product/top-new/', views.top_new, name='top_new'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
