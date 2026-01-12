import os
import sys
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')

import django
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print("Database connection successful!")
        print(f"Result: {result}")
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Please check your database credentials in the .env file")