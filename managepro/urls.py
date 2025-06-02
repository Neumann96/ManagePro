from django.contrib import admin
from django.urls import path
from . import views

# from managepro.managepro.views import main_window

urlpatterns = [
    path('', views.main_window, name='main_window'),
    path('admin/', admin.site.urls),
]
