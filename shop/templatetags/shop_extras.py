from django import template
from shop.models import Product

register = template.Library()

@register.inclusion_tag('part/single_sidebar.html')
def single_sidebar():
    latest_products = Product.objects.filter(available=True)[:4]
    return {'latest_products':latest_products}

@register.filter
def sort_form(form, num):
    return form[num-1]