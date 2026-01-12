from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'price', 'image', 'category', 'size_ml', 'weight_g', 'dimensions', 'color', 'material', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'brand': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'image': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'size_ml': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'weight_g': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'dimensions': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'color': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'material': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }