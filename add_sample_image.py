#!/usr/bin/env python
"""
Script to download a sample image and associate it with a product if no images exist.
"""
import os
import sys
import django
import requests
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essence_project.settings')
django.setup()

from perfumes.models import Product, Category

def download_sample_image():
    # Check if we have products with images
    products_with_images = Product.objects.exclude(image__isnull=True).exclude(image='')
    
    if products_with_images.exists():
        print("Products with images already exist in the database.")
        return
    
    # Get the first available product to add an image to
    product = Product.objects.first()
    if not product:
        print("No products found in the database.")
        return
    
    # Download a sample perfume image
    sample_image_url = "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"
    
    try:
        response = requests.get(sample_image_url)
        if response.status_code == 200:
            # Save the image to the media directory
            from django.core.files.base import ContentFile
            
            # Create the product_images directory if it doesn't exist
            media_path = Path("media") / "product_images"
            media_path.mkdir(parents=True, exist_ok=True)
            
            # Save the image
            image_filename = "sample_perfume.jpg"
            image_path = media_path / image_filename
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            # Update the product with the new image
            product.image.name = f"product_images/{image_filename}"
            product.save()
            
            print(f"Sample image downloaded and associated with product '{product.name}'")
        else:
            print(f"Failed to download sample image. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error downloading sample image: {str(e)}")

if __name__ == "__main__":
    download_sample_image()