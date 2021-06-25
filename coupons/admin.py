from django.contrib import admin
from .models import Coupon

# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['valid_from', 'valid_to', 'active']
    search_fields = ['code']