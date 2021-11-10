from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.SearchListView.as_view(), name='search_list'),
    path('top-sellers/', views.TopSellersView.as_view(), name='top_sellers'),
    path('recently-viewed/', views.RecentlyViewedView.as_view(), name='recently_viewed'),
    path('top-new/', views.TopNewView.as_view(), name='top_new'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list_view'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]