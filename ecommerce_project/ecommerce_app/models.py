from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

CustomUser = get_user_model()  # Using CustomUser model

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    about_item = models.TextField(blank=True, null=True)  # Field for About this item
    additional_info = models.TextField(blank=True, null=True)  # Field for Additional Information
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Allow image to be optional
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return total_rating / len(reviews)
        return None

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Ensure it uses CustomUser
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Cart)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def calculate_total_price(self):
        return sum([cart.total_price() for cart in self.products.all()])

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Ensure it uses CustomUser
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"

