from django.urls import path
from . import views
from . import views_main
from . import views_admin
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # API endpoints
    path('token/', views.custom_token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oauth/google/redirect_url/', views.get_oauth_redirect_url, name='oauth_redirect_url'),
    path('sessions/', views.exchange_code_for_session_token, name='exchange_code_for_session_token'),
    path('signup/', views.signup, name='signup'),

    # Django-based authentication pages
    path('page/', views_main.auth_page, name='auth_page'),
    # Note: signup and login are handled within the auth_page view with mode parameter
    # so we don't need separate URLs for them anymore
    path('page/logout/', views_main.logout_view, name='logout_page'),
    path('page/profile-settings/', views_main.profile_settings, name='profile_settings'),
    path('page/forgot-password/', views_main.password_reset_request, name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views_main.password_reset_confirm, name='password_reset_confirm'),

    # Admin pages
    path('admin/login/', views_admin.admin_login, name='admin_login'),
    path('admin/dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admin/edit-contact/', views_admin.edit_contact_info, name='edit_contact_info'),
    path('admin/edit-banking/', views_admin.edit_banking_details, name='edit_banking_details'),
    path('admin/developer-payment/', views_admin.developer_payment, name='developer_payment'),
    path('banking-details/<int:order_id>/', views_admin.banking_details_page, name='banking_details'),
    path('banking-details/', views_admin.banking_details_page, name='banking_details_general'),
]