from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid
# Create your models here.

class Product(models.Model):

    def get_absolute_url(self):
        return reverse("detail", args=[self.slug])
    

    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='image/')
    slug = models.SlugField(unique=True, blank=True, null=False)
    stock = models.IntegerField()
    active = models.BooleanField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    #unique_id
    sku = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    