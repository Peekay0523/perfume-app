#!/usr/bin/env python
"""
Script to check existing products and their images in the database.
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Product
import os

def check_products_and_images():
    products = Product.objects.all()
    
    print(f"Total products in database: {products.count()}")
    
    for product in products:
        print(f"\nProduct ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Brand: {product.brand}")
        print(f"Category: {product.category.name if product.category else 'No category'}")
        print(f"Has image: {bool(product.image)}")
        
        if product.image:
            print(f"Image path: {product.image.path}")
            print(f"Image URL: {product.image.url}")
            # Check if the file exists
            image_exists = os.path.exists(product.image.path)
            print(f"Image file exists: {image_exists}")
            if not image_exists:
                print(f"WARNING: Image file does not exist at {product.image.path}")
        else:
            print("No image assigned to this product")
    
    # Count products with and without images
    products_with_images = products.exclude(image__isnull=True).exclude(image='')
    products_without_images = products.filter(image__isnull=True) | products.filter(image='')
    
    print(f"\nProducts with images: {products_with_images.count()}")
    print(f"Products without images: {products_without_images.count()}")

if __name__ == "__main__":
    check_products_and_images()