from django.contrib import admin
from managepro.warehouse.models import (
    Archiveproduct, Category, Discount, Notification,
    Product, ProductDiscount, Report, ReportProduct,
    Users, Warehouse
)

admin.site.register(Archiveproduct)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Notification)
admin.site.register(Product)
admin.site.register(ProductDiscount)
admin.site.register(Report)
admin.site.register(ReportProduct)
admin.site.register(Users)
admin.site.register(Warehouse)