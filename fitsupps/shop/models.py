from django.db import models
from django.contrib.auth.models import User

# Category for organizing products
class Category(models.Model):
    name = models.CharField(max_length=100)  # Example: Protein, Vitamins, Pre-Workout

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')  # Stores uploaded product images
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Shopping Cart Item
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links cart to logged-in user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
