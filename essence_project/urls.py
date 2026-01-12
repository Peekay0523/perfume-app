"""
URL configuration for essence_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.shortcuts import redirect
import re
from perfumes import views
from authentication.views_main import main_page


def home_redirect(request):
    """Redirect to appropriate page based on authentication status"""
    if request.user.is_authenticated:
        return redirect('shop')  # Redirect logged-in users to shop
    else:
        return main_page(request)  # Show auth page for non-logged-in users


# Custom view for serving React app for non-API routes
def catch_all(request, *args, **kwargs):
    # Serve the React app for any route that is not an API route
    # API routes should be handled by the defined API paths above
    return never_cache(TemplateView.as_view(template_name='react_index.html'))(request, *args, **kwargs)


# Serve static and media files during development
if settings.DEBUG:
    # Serve media files - must be before catch-all route
    media_patterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATICFILES_DIRS in development
    static_patterns = []
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        static_patterns = static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    media_patterns = []
    static_patterns = []

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('perfumes.urls')),
    path('api/auth/', include('authentication.urls')),

    # Specific routes for Django-based app
    path('', home_redirect, name='home'),

    # Media and static files (only in debug, but defined here to maintain order)
] + media_patterns + static_patterns + [
    # Catch all other routes for React Router (must be last)
    # This ensures API routes take precedence over this catch-all
    path('<path:route>', catch_all, name='catch_all'),
]
