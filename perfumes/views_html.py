from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import Product, Category, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer
from authentication.models import ContactInfo
from django.contrib.auth import authenticate, login, logout
import json


def shop_page(request):
    """Shop page to display all products"""
    categories = Category.objects.all().order_by('name')

    # Get the category filter from URL parameters
    category_id = request.GET.get('category')

    if category_id:
        # Filter products by category
        products = Product.objects.filter(category_id=category_id).order_by('category', 'brand', 'name')
        # Update title to reflect the filter
        try:
            selected_category = Category.objects.get(id=category_id)
            title = f'{selected_category.name} Products'
        except Category.DoesNotExist:
            products = Product.objects.none()
            title = 'Products'
    else:
        products = Product.objects.all().order_by('category', 'brand', 'name')
        title = 'Our Collection'

    context = {
        'categories': categories,
        'products': products,
        'title': title,
        'selected_category_id': int(category_id) if category_id else None
    }
    return render(request, 'shop.html', context)


def product_detail(request, product_id):
    """Product detail page for a specific product"""
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'product.html', context)


@login_required
def cart_page(request):
    """Cart page to display items in the user's cart"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    # Calculate total price for each item
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    subtotal = sum(item.total_price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'title': 'Shopping Cart'
    }
    return render(request, 'cart.html', context)


@login_required
def checkout_page(request):
    """Checkout page for placing an order"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', request.user.username)
        customer_email = request.POST.get('customer_email', request.user.email)
        delivery_method = request.POST.get('delivery_method', 'shipping')

        # Validate delivery method
        if delivery_method not in ['shipping', 'pickup', 'pep_paxi']:
            delivery_method = 'shipping'  # Default fallback

        # Determine shipping address based on delivery method
        shipping_address = ""
        if delivery_method == 'shipping':
            shipping_address = request.POST.get('shipping_address', '').strip()
            if not shipping_address:
                messages.error(request, 'Please provide a shipping address')
                context = {
                    'cart_items': cart_items,
                    'subtotal': subtotal,
                    'title': 'Checkout',
                    'user': request.user
                }
                return render(request, 'checkout.html', context)
        elif delivery_method == 'pickup':
            # For pickup, use a default address or the store address
            contact_info = ContactInfo.objects.first()
            if contact_info:
                shipping_address = f"{contact_info.address}, {contact_info.city}, {contact_info.state} {contact_info.zip_code} (Store Pickup)"
            else:
                shipping_address = "123 Luxury Avenue, New York, NY 10001 (Store Pickup)"
        elif delivery_method == 'pep_paxi':
            # For PEP/PAXI delivery, get the selected city and mall
            pep_city = request.POST.get('pep_city', '').strip()
            pep_mall = request.POST.get('pep_mall', '').strip()

            if not pep_city or not pep_mall:
                messages.error(request, 'Please select a city and specify the mall for PEP/PAXI collection')
                context = {
                    'cart_items': cart_items,
                    'subtotal': subtotal,
                    'title': 'Checkout',
                    'user': request.user
                }
                return render(request, 'checkout.html', context)

            # Create the shipping address based on city and mall
            city_names = {
                'cape_town': 'Cape Town',
                'johannesburg': 'Johannesburg',
                'pretoria': 'Pretoria',
                'durban': 'Durban',
                'port_elizabeth': 'Port Elizabeth',
                'bloemfontein': 'Bloemfontein',
                'east_london': 'East London',
                'polokwane': 'Polokwane',
                'kimberley': 'Kimberley',
                'upington': 'Upington',
            }

            city_name = city_names.get(pep_city, pep_city.title())
            shipping_address = f"PEP Branch at {pep_mall}, {city_name} (PEP/PAXI Collection Point)"

        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total=subtotal,
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

                messages.success(request, 'Order placed successfully!')
                return redirect('banking_details', order_id=order.id)
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'title': 'Checkout',
        'user': request.user
    }
    return render(request, 'checkout.html', context)


@login_required
def orders_page(request):
    """Page to display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        'title': 'My Orders'
    }
    return render(request, 'orders.html', context)


@login_required
def order_detail(request, order_id):
    """Page to display details of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    # Calculate total price for each order item
    for item in order_items:
        item.total_price = item.price * item.quantity

    context = {
        'order': order,
        'order_items': order_items,
        'title': f'Order #{order.id}'
    }
    return render(request, 'order_detail.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Add a product to the user's cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

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

    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', product_id=product_id)


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, cart_item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


def index_page(request):
    """Home page - just redirects to shop if authenticated"""
    if request.user.is_authenticated:
        return redirect('shop')
    else:
        # For now, redirect to auth page if not authenticated
        # In a real app, you might want a proper landing page
        from authentication.views_main import main_page
        return main_page(request)