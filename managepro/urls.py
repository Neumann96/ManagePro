from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# from managepro.managepro.views import main_window

urlpatterns = [
    path('', views.main_window, name='main_window'),
    path('admin/', admin.site.urls),
    path('products/', views.views_products, name='view_products'),
    path('categories/', views.views_categories, name='view_categories'),
    path('warehouse/', views.warehouse_list, name='view_warehouse')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
