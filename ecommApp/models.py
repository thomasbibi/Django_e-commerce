from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Import Django's built-in User model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.phone}"

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_img/")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - ${self.price}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')  # Updated to use built-in User
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in {self.cart}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Updated to use built-in User
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order {self.order.id}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment for Order {self.order.id}"