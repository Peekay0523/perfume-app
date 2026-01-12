from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, CartItem, Order, OrderItem
from .forms import ProductForm, CategoryForm
from authentication.models import ContactInfo, BankingDetails
from authentication.utils import send_order_status_update


@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard"""
    # Get or create contact info instance
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,
        defaults={
            'address': '123 Luxury Avenue',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'email': 'contact@essence.com',
            'phone': '+1 (555) 123-4567',
        }
    )

    # Get or create banking details instance
    banking_details, created = BankingDetails.objects.get_or_create(
        id=1,
        defaults={
            'bank_name': 'Standard Bank',
            'account_holder_name': 'Essence Luxury Boutique',
            'account_number': '0000000000',
            'branch_code': '000000',
            'branch_name': 'Sandton City',
            'swift_code': 'SBZAZAJJ',
            'reference_instruction': 'Use your order number as reference'
        }
    )

    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_carts = CartItem.objects.count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_carts': total_carts,
        'contact_info': contact_info,
        'banking_details': banking_details,
    }
    return render(request, 'admin_dashboard.html', context)


@staff_member_required
def manage_users(request):
    """Manage all users"""
    users = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin_users.html', context)


@staff_member_required
def manage_products(request):
    """Manage products"""
    products = Product.objects.all().order_by('-created_at')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin_products.html', context)


@staff_member_required
def edit_product(request, product_id=None):
    """Edit or create a product"""
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES or None, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'admin_edit_product.html', context)


@staff_member_required
def manage_categories(request):
    """Manage product categories"""
    categories = Category.objects.all().order_by('name')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin_categories.html', context)


@staff_member_required
def edit_category(request, category_id=None):
    """Edit or create a category"""
    if category_id:
        category = get_object_or_404(Category, id=category_id)
    else:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'admin_edit_category.html', context)


@staff_member_required
def manage_orders(request):
    """Manage orders"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_email__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]
    
    context = {
        'orders': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'statuses': statuses,
    }
    return render(request, 'admin_orders.html', context)


@staff_member_required
def manage_cart(request):
    """Manage cart items"""
    cart_items = CartItem.objects.all().order_by('-created_at')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        cart_items = cart_items.filter(
            Q(user__username__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(product__brand__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(cart_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cart_items': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin_cart.html', context)


@staff_member_required
def toggle_user_active(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'success': True, 'is_active': user.is_active})


@staff_member_required
def delete_order(request, order_id):
    """Delete an order"""
    try:
        order = get_object_or_404(Order, id=order_id)
        order_id = order.id  # Store ID for the success message
        order.delete()
        return JsonResponse({'success': True, 'message': f'Order {order_id} deleted successfully'})
    except Exception as e:
        print(f"Error deleting order: {str(e)}")
        return JsonResponse({'success': False, 'error': f'Error deleting order: {str(e)}'})


@staff_member_required
def update_order_status(request, order_id):
    """Update order status"""
    try:
        order = get_object_or_404(Order, id=order_id)
        old_status = order.status
        new_status = request.POST.get('status')

        if new_status in [choice[0] for choice in Order.ORDER_STATUS_CHOICES]:
            order.status = new_status
            order.save()

            # Send email notification to customer about status change
            try:
                send_order_status_update(
                    user_email=order.customer_email or order.user.email,
                    order_id=order.id,
                    new_status=new_status
                )
            except Exception as email_error:
                # Log the error but don't fail the status update if email sending fails
                print(f"Error sending order status update email: {str(email_error)}")

            return JsonResponse({'success': True, 'status': order.status})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Exception as e:
        print(f"Error updating order status: {str(e)}")
        return JsonResponse({'success': False, 'error': f'Error updating status: {str(e)}'})