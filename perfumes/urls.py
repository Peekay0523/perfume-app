from django.urls import path
from . import views
from . import views_html
from . import views_admin

urlpatterns = [
    # HTML pages
    path('', views_html.shop_page, name='shop'),
    path('product/<int:product_id>/', views_html.product_detail, name='product_detail'),
    path('cart/', views_html.cart_page, name='cart'),
    path('checkout/', views_html.checkout_page, name='checkout'),
    path('orders/', views_html.orders_page, name='orders'),
    path('orders/<int:order_id>/', views_html.order_detail, name='order_detail'),

    # Cart actions
    path('product/<int:product_id>/add/', views_html.add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_item_id>/remove/', views_html.remove_from_cart, name='remove_from_cart'),

    # API endpoints (for AJAX calls and API access)
    path('api/products/', views.get_products, name='get_products'),
    path('api/products/<int:product_id>/', views.get_product, name='get_product'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/categories/<int:category_id>/products/', views.get_products_by_category, name='get_products_by_category'),

    # Cart API endpoints
    path('api/cart/', views.get_cart, name='get_cart_api'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart_api'),
    path('api/<int:cart_item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('api/<int:cart_item_id>/delete/', views.remove_from_cart, name='remove_from_cart_api'),

    # Order API endpoints
    path('api/orders/', views.get_orders, name='get_orders_api'),
    path('api/orders/<int:order_id>/', views.get_order, name='get_order_api'),
    path('api/orders/create/', views.create_order, name='create_order_api'),

    # User API endpoints
    path('api/users/me/', views.get_current_user, name='get_current_user'),
    path('api/logout/', views.logout_user, name='logout_user_api'),

    # Admin section URLs
    path('admin/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views_admin.manage_users, name='manage_users'),
    path('admin/products/', views_admin.manage_products, name='manage_products'),
    path('admin/products/edit/<int:product_id>/', views_admin.edit_product, name='edit_product'),
    path('admin/products/create/', views_admin.edit_product, name='create_product'),
    path('admin/categories/', views_admin.manage_categories, name='manage_categories'),
    path('admin/categories/edit/<int:category_id>/', views_admin.edit_category, name='edit_category'),
    path('admin/categories/create/', views_admin.edit_category, name='create_category'),
    path('admin/orders/', views_admin.manage_orders, name='manage_orders'),
    path('admin/cart/', views_admin.manage_cart, name='manage_cart'),
    path('admin/user/<int:user_id>/toggle/', views_admin.toggle_user_active, name='toggle_user_active'),
    path('admin/order/<int:order_id>/update/', views_admin.update_order_status, name='update_order_status'),
    path('admin/order/<int:order_id>/delete/', views_admin.delete_order, name='delete_order'),
]