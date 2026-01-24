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
    # Include product details in the order item
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_brand = serializers.CharField(source='product.brand', read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_image = serializers.SerializerMethodField()
    product_size_ml = serializers.IntegerField(source='product.size_ml', read_only=True)
    product_weight_g = serializers.IntegerField(source='product.weight_g', read_only=True)
    product_dimensions = serializers.CharField(source='product.dimensions', read_only=True)
    product_color = serializers.CharField(source='product.color', read_only=True)
    product_material = serializers.CharField(source='product.material', read_only=True)
    product_notes = serializers.CharField(source='product.notes', read_only=True)
    product_category = serializers.StringRelatedField(source='product.category', read_only=True)

    def get_product_image(self, obj):
        if obj.product.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_id', 'quantity', 'price', 'created_at', 'updated_at',
            'product_name', 'product_brand', 'product_description', 'product_price',
            'product_image', 'product_size_ml', 'product_weight_g', 'product_dimensions',
            'product_color', 'product_material', 'product_notes', 'product_category'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = ['user']  # Exclude the user field for security


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'shipping_address', 'total', 'delivery_method', 'payment_method']