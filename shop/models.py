from django.db import models
from django.db.models.fields import related
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


def upload_image(instance, filename):
    return f'images/{instance.name}/{filename}'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='Products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to=upload_image, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(null=True, blank=True)
    sales_number = models.PositiveIntegerField(null=True, blank=True, default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

def upload_gallery_image(instance, filename):
    return f'images/{instance.product.name}/gallery/{filename}'

class ProductGallery(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image)
    product = models.ForeignKey('Product', related_name='gallery', on_delete=models.CASCADE, null=True, blank=True)