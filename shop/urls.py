from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/category/<slug:slug>/', views.ProductListView.as_view(), name='product_list_view'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
