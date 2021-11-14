import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, product_ids):
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        suggested_products = None
        if products:
            suggestions = r.zrange(
            self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
            suggested_products_ids = [int(id) for id in suggestions]
            suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
            suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))