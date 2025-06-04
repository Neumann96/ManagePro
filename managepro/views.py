from django.db.models.signals import post_save
from django.shortcuts import render
from unicodedata import category

from django.db.models import Count
from .models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


def main_window(request):
    return render(request, 'main.html')


def views_products(request):
    products = Product.objects.filter(image__isnull=False).exclude(image='')
    return render(request, 'products.html', {'products': products})


def views_categories(request):
    query = request.GET.get('search', '')

    # Поиск категорий по имени
    category = Category.objects.filter(categoryname__icontains=query).order_by('categoryname').distinct()

    # Агрегатная функция — сколько продуктов в каждой категории
    category_with_counts = Category.objects.annotate(product_count=Count('product')).order_by('categoryname')

    return render(request, 'categories.html', {
        'category': category,
        'category_with_counts': category_with_counts,
        'query': query,
    })