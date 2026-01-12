from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer


def home(request):
    """Home page view"""
    return render(request, 'index.html', {'title': 'Essence - Luxury Boutique'})


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all().order_by('category', 'brand', 'name')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all().order_by('name')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id).order_by('brand', 'name')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not product_id or not quantity:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    product = get_object_or_404(Product, id=product_id)

    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += quantity
        cart_item.save()

    return Response({'success': True}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'Missing quantity'}, status=status.HTTP_400_BAD_REQUEST)

    cart_item.quantity = quantity
    cart_item.save()

    return Response({'success': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return Response({'success': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    customer_name = request.data.get('customer_name')
    customer_email = request.data.get('customer_email')
    shipping_address = request.data.get('shipping_address')
    delivery_method = request.data.get('delivery_method', 'shipping')

    if not customer_name or not customer_email or not shipping_address:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Get cart items for the user
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create order
    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total=total,
            delivery_method=delivery_method,
            customer_name=customer_name,
            customer_email=customer_email,
            shipping_address=shipping_address
        )

        # Create order items and clear cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear cart
        cart_items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    }
    return Response(user_data)


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'success': True}, status=status.HTTP_200_OK)