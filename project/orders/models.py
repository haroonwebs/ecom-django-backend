from django.db import models
from accounts.models import User
from products.models import Product


class Order(models.Model):
    
    STATUS_CHOICES= (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user= models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    total_price= models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    order_status= models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    shipping_address= models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"order #{self.Order.id} - {self.user.email}"
    

   

 # order items model
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

