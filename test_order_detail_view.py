import os
import sys
import django

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Order, OrderItem, Product, Category
from django.contrib.auth.models import User
from django.template import Context, Template
from perfumes.views_html import order_detail
from django.http import HttpRequest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import login
from unittest.mock import MagicMock

def test_order_detail_view():
    try:
        # Get the first user
        user = User.objects.first()
        if not user:
            print("No users found in the database")
            return
        
        # Get an existing order or create one
        order = Order.objects.filter(user=user).first()
        if not order:
            # Create a test order if none exists
            category, created = Category.objects.get_or_create(name="Test Category", slug="test-category")
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
            
            order = Order.objects.create(
                user=user,
                total=29.99,
                customer_name="Test Customer",
                customer_email="test@example.com",
                shipping_address="123 Test Street"
            )
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=29.99
            )
        
        print(f"Testing order ID: {order.id}")
        
        # Create a mock request
        request = HttpRequest()
        request.user = user
        request.method = 'GET'
        
        # Add session support to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        
        # Call the order_detail view
        response = order_detail(request, order.id)
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("Order detail view works correctly!")
        else:
            print(f"Error: {response.status_code}")
        
    except Exception as e:
        print(f"Error testing order detail view: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_order_detail_view()