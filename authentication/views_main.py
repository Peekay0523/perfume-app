from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
import json


def main_page(request):
    """Main page view that handles both landing page and auth forms based on URL parameters"""
    context = {}

    # Add features to context to show on landing page
    context['features'] = [
        {'title': 'Authentic Products', 'desc': 'Only genuine luxury fragrances from authorized distributors'},
        {'title': 'Free Shipping', 'desc': 'Complimentary shipping on all orders over $100'},
        {'title': 'Expert Curation', 'desc': 'Hand-selected by our team of fragrance specialists'}
    ]

    # Handle auth forms if mode is specified
    if request.GET.get('mode') == 'signup':
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Validation
            if not username or not email or not password:
                messages.error(request, 'All fields are required.')
                return render(request, 'react_index.html', context)

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'react_index.html', context)

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return render(request, 'react_index.html', context)

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'react_index.html', context)

            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'react_index.html', context)

            # Create user
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                auth_login(request, user)  # Log the user in after signup
                messages.success(request, 'Account created successfully!')
                return redirect('shop')  # Redirect to shop page to clear the form
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return render(request, 'react_index.html', context)
        # If it's just a GET request with mode=signup, show the form with the mode in context
        context['show_signup'] = True

    elif request.GET.get('mode') == 'login':
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('shop')  # Redirect to shop page to clear the form
            else:
                messages.error(request, 'Invalid username or password.')
        # If it's just a GET request with mode=login, show the form with the mode in context
        context['show_login'] = True

    elif request.method == 'POST' and 'logout' in request.path:
        # Handle logout if this is the logout view
        auth_logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('home')

    return render(request, 'react_index.html', context)


def shop_page(request):
    """Shop page view"""
    context = {
        'features': [
            {'title': 'Authentic Products', 'desc': 'Only genuine luxury fragrances from authorized distributors'},
            {'title': 'Free Shipping', 'desc': 'Complimentary shipping on all orders over $100'},
            {'title': 'Expert Curation', 'desc': 'Hand-selected by our team of fragrance specialists'}
        ]
    }
    return render(request, 'react_index.html', context)




@login_required
def logout_view(request):
    """Django-based logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def password_reset_request(request):
    """Password reset request page"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')

        # Find user by username or email
        user = None
        if '@' in username_or_email:
            # If contains @, treat as email
            # Use filter() to avoid MultipleObjectsReturned and get the first user
            user_queryset = User.objects.filter(email=username_or_email)
            if user_queryset.exists():
                user = user_queryset.first()  # Get the first user with that email
        else:
            # Otherwise treat as username
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                pass

        if user:
            # Generate password reset token and URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create the reset link using the correct URL
            reset_link = request.build_absolute_uri(f'/api/auth/password-reset/{uid}/{token}/')

            # Send email with reset link
            try:
                subject = 'Password Reset Request - Essence'
                html_message = render_to_string('emails/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                    'site_name': 'Essence Luxury Perfumes'
                })

                send_mail(
                    subject=subject,
                    message='',  # Plain text version
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )

                messages.success(request, 'Password reset instructions have been sent to your email address.')
                return redirect('auth_page')
            except Exception as e:
                messages.error(request, f'Error sending reset email: {str(e)}')
        else:
            messages.error(request, 'No account found with that username or email.')

    context = {
        'title': 'Forgot Password',
    }
    return render(request, 'password_reset_request.html', context)


def password_reset_confirm(request, uidb64, token):
    """Password reset confirmation page"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth import get_user_model
    from django.contrib import messages

    try:
        # Decode the user id
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password and new_password == confirm_password:
                if len(new_password) < 6:
                    messages.error(request, 'Password must be at least 6 characters long.')
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Your password has been reset successfully. You can now sign in.')
                    return redirect('auth_page')
            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'password_reset_confirm.html', {
            'valid_token': True,
            'title': 'Reset Your Password'
        })
    else:
        return render(request, 'password_reset_confirm.html', {
            'valid_token': False,
            'title': 'Invalid Reset Link'
        })


def profile_settings(request):
    """User profile settings page"""
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('auth_page')

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Update user information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        # Check if username is being updated and if it's available
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken.')
            else:
                user.username = username

        # Handle password change if provided
        if current_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password:
                if new_password != confirm_new_password:
                    messages.error(request, 'New passwords do not match.')
                elif len(new_password) < 6:
                    messages.error(request, 'Password must be at least 6 characters long.')
                else:
                    user.set_password(new_password)

        try:
            user.save()
            # If password was changed, update session to maintain login
            if current_password and new_password:
                auth_login(request, user)
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

    context = {
        'title': 'Account Settings',
    }
    return render(request, 'profile_settings.html', context)


def auth_page(request):
    """Combined authentication page with both login and signup options"""
    context = {}

    # Handle form submissions regardless of mode parameter
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            # Check if this is a login or signup by looking at mode parameter from the form submission
            mode = request.GET.get('mode', 'login')  # Default to login if no mode specified

            if mode == 'signup':
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                # Validation
                if not username or not email or not password:
                    messages.error(request, 'All fields are required.')
                    return render(request, 'authentication/auth.html', context)

                if password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'authentication/auth.html', context)

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                    return render(request, 'authentication/auth.html', context)

                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered.')
                    return render(request, 'authentication/auth.html', context)

                if len(password) < 6:
                    messages.error(request, 'Password must be at least 6 characters long.')
                    return render(request, 'authentication/auth.html', context)

                # Create user
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    auth_login(request, user)  # Log the user in after signup
                    messages.success(request, 'Account created successfully!')
                    return redirect('shop')  # Redirect to shop page
                except Exception as e:
                    messages.error(request, f'Error creating account: {str(e)}')
                    return render(request, 'authentication/auth.html', context)
            else:  # login mode
                username = request.POST.get('username')
                password = request.POST.get('password')

                # First, try authenticating with the entered username
                user = authenticate(request, username=username, password=password)

                # If that doesn't work, try treating it as an email
                if user is None:
                    # Check if the input looks like an email
                    if '@' in username:
                        # Try to get the user by email, then authenticate
                        try:
                            user_from_email = User.objects.get(email=username)
                            user = authenticate(request, username=user_from_email.username, password=password)
                        except User.DoesNotExist:
                            user = None

                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('shop')  # Redirect to shop page
                else:
                    messages.error(request, 'Invalid username or password.')

    return render(request, 'authentication/auth.html', context)