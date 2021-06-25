from django.contrib import admin
from .models import Category, Product, ProductGallery

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name', )}

class ImageInlines(admin.TabularInline):
    model = ProductGallery

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_percent', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'discount_percent', 'available']
    prepopulated_fields = {'slug':('name',)}
    inlines = [
        ImageInlines,
    ]