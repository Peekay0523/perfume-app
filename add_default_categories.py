#!/usr/bin/env python
"""
Script to add default categories to the database: perfume, electronics, and clothing.
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Category

def add_default_categories():
    default_categories = [
        {
            'name': 'Perfume',
            'description': 'Luxury perfumes and fragrances',
            'slug': 'perfume'
        },
        {
            'name': 'Electronics',
            'description': 'Electronic devices and gadgets',
            'slug': 'electronics'
        },
        {
            'name': 'Clothing',
            'description': 'Fashionable clothing and apparel',
            'slug': 'clothing'
        }
    ]

    for cat_data in default_categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': cat_data['slug']
            }
        )
        
        if created:
            print(f"Created category: {cat_data['name']}")
        else:
            print(f"Category already exists: {cat_data['name']}")

if __name__ == "__main__":
    add_default_categories()