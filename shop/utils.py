from django.db.models import Count

def best_selling_products(qs, num=None):
    top_sellers_count = qs.values_list('id').annotate(count=Count('order_items')).order_by('-count')[:num]
    product_ids = [item[0] for item in top_sellers_count]
    return product_ids

def top_new_ids(redis, num=None):
    list_ids = redis.hgetall('product_visit')
    list_ids = sorted(list_ids.items(), key=lambda d: int(d[1]), reverse=True)[:num]
    return [item[0] for item in list_ids]

def inOrder(nums, num):
    nums = map(int, nums)
    ids = []
    for x in nums:
        if x not in ids and len(ids) < num:
            ids.append(x)
    return ids