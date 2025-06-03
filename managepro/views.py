from django.db.models.signals import post_save
from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


def main_window(request):
    return render(request, 'main.html')


def views_products(request):
    return render(request, 'base.html')