from django.db.models.signals import post_save
from django.shortcuts import render
from unicodedata import category
from django.utils.dateparse import parse_datetime
from django.db.models import Count
from .models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect


def main_window(request):
    return render(request, 'main.html')


def views_products(request):
    # if request.method == "POST":
    #     productname = request.POST.get("productname")
    #     categoryid = request.POST.get("categoryid") or None
    #     quantity = request.POST.get("quantity") or None
    #     expirydate = request.POST.get("expirydate") or None
    #     price = request.POST.get("price") or None
    #     datereceived = request.POST.get("datereceived") or None
    #     warehouseid_input = request.POST.get("warehouseid") or None
    #     try:
    #         warehouse = Warehouse.objects.get(pk=warehouseid_input) if warehouseid_input else None
    #     except Warehouse.DoesNotExist:
    #         warehouse = None
    #     image = request.FILES.get("image")
    #
    #     product = Product(
    #         productname=productname,
    #         categoryid=Category.objects.get(pk=categoryid) if categoryid else None,
    #         quantity=quantity,
    #         expirydate=expirydate or None,
    #         price=price,
    #         datereceived=parse_datetime(datereceived) if datereceived else None,
    #         warehouseid=warehouse,
    #         image=image,
    #     )
    #     product.save()
    #     return redirect('view_products')
    # warehouses = Warehouse.objects.all()
    products = Product.objects.filter(image__isnull=False).exclude(image='')
    return render(request, 'products.html', {
        'products': products,
    })

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


def warehouse_list(request):
    query = request.GET.get('search')
    if query:
        warehouses = Warehouse.objects.filter(address__icontains=query)
    else:
        warehouses = Warehouse.objects.all()

    return render(request, 'warehouse.html', {
        'warehouses': warehouses,
        'query': query
    })


def product_detail(request, productid):
    product = get_object_or_404(Product, productid=productid)

    if request.method == 'POST':
        product.productname = request.POST.get('productname')
        product_price = request.POST.get('price')
        if product_price:
            product.price = product_price
        product.save()
        return redirect('product_detail', productid=product.productid)

    # Явное преобразование Decimal в float для корректного отображения в input
    price_value = float(product.price) if product.price is not None else ''
    price_value = str(price_value).replace(',', '.')
    return render(request, 'product_detail.html', {
        'product': product,
        'price_value': price_value
    })


def delete_product(request, productid):
    if request.method == "POST":
        product = get_object_or_404(Product, productid=productid)
        product.delete()
    return redirect('view_products')

def add_product(request):
    if request.method == "POST":
        productname = request.POST.get("productname")
        categoryid = request.POST.get("categoryid") or None
        quantity = request.POST.get("quantity") or None
        expirydate = request.POST.get("expirydate") or None
        price = request.POST.get("price") or None
        datereceived = request.POST.get("datereceived") or None
        warehouseid_input = request.POST.get("warehouseid") or None
        try:
            warehouse = Warehouse.objects.get(pk=warehouseid_input) if warehouseid_input else None
        except Warehouse.DoesNotExist:
            warehouse = None
        image = request.FILES.get("image")

        product = Product(
            productname=productname,
            categoryid=Category.objects.get(pk=categoryid) if categoryid else None,
            quantity=quantity,
            expirydate=expirydate or None,
            price=price,
            datereceived=parse_datetime(datereceived) if datereceived else None,
            warehouseid=warehouse,
            image=image,
        )
        product.save()
        return redirect('view_products')
    warehouses = Warehouse.objects.all()
    products = Product.objects.filter(image__isnull=False).exclude(image='')
    return render(request, 'add_product.html', {
        'products': products,
        'warehouses': warehouses
    })