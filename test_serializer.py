import os
import sys
import django

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Order, OrderItem
from django.contrib.auth.models import User
from perfumes.serializers import OrderSerializer
from django.core.exceptions import ObjectDoesNotExist

def test_serializer_output():
    # Get the first user to test with
    try:
        user = User.objects.first()
        if not user:
            print("No users found in the database")
            return
            
        print(f"Using user: {user.username}")
        
        # Get orders for this user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        print(f"Found {orders.count()} orders for user {user.username}")
        
        if orders.exists():
            first_order = orders.first()
            print(f"Testing order ID: {first_order.id}")
            
            # Serialize the order
            serializer = OrderSerializer(first_order)
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
        else:
            print("No orders found for this user")
            
    except Exception as e:
        print(f"Error testing serializer: {e}")

if __name__ == "__main__":
    test_serializer_output()