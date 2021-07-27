from django.core.cache import cache
from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver
from .models import Product, Slider

@receiver([post_save, post_delete], sender=Product)
def remove_product_cache(sender, **kwargs):
    cache.delete('products')

@receiver([post_save, post_delete], sender=Slider)
def remove_slider_cache(sender, **kwargs):
    cache.delete('sliders')