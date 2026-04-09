from django.db import models
from django.contrib.auth.models import User
from myapp.models import Product
import secrets
import string
import time

# Create your models here.

def generate_untraceable_id():
    timestamp = hex(int(time.time()))[2:].upper() 
    
    alphabet = string.ascii_uppercase + string.digits
    alphabet = alphabet.replace('O','').replace('0','').replace('I','').replace('1','')
    random_part = ''.join(secrets.choice(alphabet) for _ in range(6))
    
    return f"{timestamp}{random_part}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #unique_order_id
    order_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            new_id = generate_untraceable_id()
            while Order.objects.filter(order_id=new_id).exists():
                new_id = generate_untraceable_id()
            self.order_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.order_id} | User: {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
