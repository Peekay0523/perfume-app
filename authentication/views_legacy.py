from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

def signup_view(request):
    """Django-based signup view as an alternative to React form"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'authentication/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'authentication/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'authentication/signup.html')
        
        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)  # Log the user in after signup
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Redirect to home page
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'authentication/signup.html')
    
    return render(request, 'authentication/signup.html')

def login_view(request):
    """Django-based login view as an alternative to React form"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            
            # Redirect to next page if provided, otherwise to home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')

@login_required
def logout_view(request):
    """Django-based logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def auth_page(request):
    """Combined authentication page with both login and signup options"""
    return render(request, 'authentication/auth.html')