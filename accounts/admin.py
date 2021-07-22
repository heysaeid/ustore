from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'address', 'city', 'county', 'phone']
    list_filter = ['city', 'county']