from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s cart"



# cart items model
class CartItem(models.Model):
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"