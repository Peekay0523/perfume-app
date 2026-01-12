from rest_framework import serializers
from .models import Product, Category, CartItem, Order, OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    # Include product details in the cart item
    name = serializers.CharField(source='product.name', read_only=True)
    brand = serializers.CharField(source='product.brand', read_only=True)
    description = serializers.CharField(source='product.description', read_only=True)
    price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    image = serializers.ImageField(source='product.image', read_only=True)
    size_ml = serializers.IntegerField(source='product.size_ml', read_only=True)
    weight_g = serializers.IntegerField(source='product.weight_g', read_only=True)
    dimensions = serializers.CharField(source='product.dimensions', read_only=True)
    color = serializers.CharField(source='product.color', read_only=True)
    material = serializers.CharField(source='product.material', read_only=True)
    notes = serializers.CharField(source='product.notes', read_only=True)
    category = serializers.StringRelatedField(source='product.category', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product_id', 'name', 'brand', 'description', 'price', 'image', 'size_ml', 'weight_g', 'dimensions', 'color', 'material', 'notes', 'category']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'shipping_address', 'total', 'delivery_method']