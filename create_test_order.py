import os
import sys
import django

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Order, OrderItem, Product, Category
from django.contrib.auth.models import User
from perfumes.serializers import OrderSerializer
from django.db import transaction

def create_test_order():
    try:
        # Get the first user
        user = User.objects.first()
        if not user:
            print("No users found in the database")
            return
        
        # Get or create a category
        category, created = Category.objects.get_or_create(name="Test Category", slug="test-category")
        
        # Get or create a product
        product, created = Product.objects.get_or_create(
            name="Test Product",
            brand="Test Brand",
            price=29.99,
            category=category,
            defaults={
                'description': 'Test product description',
                'size_ml': 100
            }
        )
        
        # Create an order
        order = Order.objects.create(
            user=user,
            total=29.99,
            customer_name="Test Customer",
            customer_email="test@example.com",
            shipping_address="123 Test Street"
        )
        
        # Create an order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=29.99
        )
        
        print(f"Created order ID: {order.id} with order item ID: {order_item.id}")
        
        # Test the serializer
        serializer = OrderSerializer(order)
        serialized_data = serializer.data
        
        print("Serialized order data:")
        import json
        print(json.dumps(serialized_data, indent=2, default=str))
        
        # Check if product images are included in the response
        if 'items' in serialized_data and serialized_data['items']:
            first_item = serialized_data['items'][0]
            if 'product_image' in first_item:
                print(f"\nSuccess! Product image found: {first_item['product_image']}")
            else:
                print("\nProduct image field not found in response")
        else:
            print("\nNo items found in the order")
        
    except Exception as e:
        print(f"Error creating test order: {e}")

if __name__ == "__main__":
    create_test_order()