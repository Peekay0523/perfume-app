from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_token_obtain_pair(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        tokens = get_tokens_for_user(user)

        # Set tokens in cookies for frontend access
        response = Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)

        return response
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

# OAuth redirect URL endpoint - matches expected endpoint by React app
@api_view(['GET'])
@permission_classes([AllowAny])
def get_oauth_redirect_url(request):
    # This should return the actual Google OAuth URL
    # In a real implementation, you'd configure these in settings
    client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', 'YOUR_CLIENT_ID')
    if client_id == 'YOUR_CLIENT_ID':
        # If not configured, return an error
        return Response(
            {'error': 'Google OAuth not configured'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    redirect_uri = request.build_absolute_uri('/api/auth/callback')  # Correct callback URL
    scope = "openid email profile"
    auth_url = f"https://accounts.google.com/o/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"

    return Response({'redirectUrl': auth_url}, status=status.HTTP_200_OK)


# Exchange OAuth code for session token - matches expected endpoint by React app
@api_view(['POST'])
@permission_classes([AllowAny])
def exchange_code_for_session_token(request):
    """
    Exchanges OAuth code for a session token.
    This endpoint is called by the React app after OAuth redirect.
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'No authorization code provided'}, status=status.HTTP_400_BAD_REQUEST)

    # In a real implementation, you'd exchange the code with Google's token endpoint
    # For now, we'll simulate the process with basic user creation
    # This should integrate with a proper OAuth library

    # For demo purposes, we'll create a default user
    # In real implementation, you'd get user info from Google's userinfo endpoint after code exchange
    username = request.data.get('username', f'oauth_user_{hash(code) % 10000}')
    email = request.data.get('email', f'{username}@example.com')

    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': 'OAuth', 'last_name': 'User'}
    )

    login(request, user)
    tokens = get_tokens_for_user(user)

    # Return tokens - React app expects session token in response
    return Response({'sessionToken': str(tokens['access'])}, status=status.HTTP_200_OK)


# Signup endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    tokens = get_tokens_for_user(user)

    return Response({
        'refresh': tokens['refresh'],
        'access': tokens['access'],
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    }, status=status.HTTP_201_CREATED)