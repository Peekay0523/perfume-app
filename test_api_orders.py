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
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory

def test_api_orders_with_context():
    try:
        # Get the first user
        user = User.objects.first()
        if not user:
            print("No users found in the database")
            return
        
        # Get an existing order or create one
        order = Order.objects.filter(user=user).first()
        if not order:
            print("No orders found for this user")
            return
        
        print(f"Testing API serialization for order ID: {order.id}")
        
        # Create a request factory to simulate request context
        factory = RequestFactory()
        request = factory.get('/api/orders/')  # Simulate the API endpoint
        
        # Serialize the order with request context
        serializer = OrderSerializer(instance=order, context={'request': request})
        serialized_data = serializer.data
        
        print("Serialized order data from API:")
        import json
        print(json.dumps(serialized_data, indent=2, default=str))
        
        # Check if product images are included in the response
        if 'items' in serialized_data and serialized_data['items']:
            first_item = serialized_data['items'][0]
            if 'product_image' in first_item:
                print(f"\nSuccess! Product image found in API response: {first_item['product_image']}")
                
                # Check if it's a proper URL
                image_url = first_item['product_image']
                if image_url and image_url.startswith('http'):
                    print("✓ Image URL is properly formatted with full domain")
                elif image_url is None:
                    print("⚠ Product has no image (which is OK)")
                else:
                    print("? Image URL format might need review")
            else:
                print("\n❌ Product image field not found in API response")
        else:
            print("\nNo items found in the order")
        
    except Exception as e:
        print(f"Error testing API serialization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_orders_with_context()