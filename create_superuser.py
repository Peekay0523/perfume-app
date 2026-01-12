import os
import sys
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if superuser already exists
if User.objects.filter(username='admin').exists():
    print("Superuser 'admin' already exists")
else:
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"Superuser 'admin' created successfully with ID: {user.id}")
    
# Count superusers
superuser_count = User.objects.filter(is_superuser=True).count()
print(f"Total superusers in database: {superuser_count}")