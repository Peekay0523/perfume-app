from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the category name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    size_ml = models.IntegerField(null=True, blank=True)  # For perfumes
    weight_g = models.IntegerField(null=True, blank=True)  # For other products
    dimensions = models.CharField(max_length=255, null=True, blank=True)  # For other products
    color = models.CharField(max_length=100, null=True, blank=True)  # For other products
    material = models.CharField(max_length=255, null=True, blank=True)  # For other products
    notes = models.TextField(null=True, blank=True)  # For perfumes
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"

    class Meta:
        ordering = ['category', 'name']


class Perfume(Product):
    """Specific model for perfumes that inherits from Product"""

    class Meta:
        proxy = True  # This makes Perfume use the same table as Product but with different behavior


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.user.username}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('shipping', 'Home Delivery'),
        ('pickup', 'Store Pickup'),
        ('pep_paxi', 'PEP/PAXI Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default='shipping')
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - ${self.total}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in order {self.order.id}"