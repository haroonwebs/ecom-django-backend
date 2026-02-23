from django.db import models
from categories.models import Category

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=255, null=False)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    product_image=models.ImageField(upload_to="products/", blank=True, null=True)
    is_available=models.BooleanField(default=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
