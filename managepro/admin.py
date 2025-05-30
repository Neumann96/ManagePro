from django.contrib import admin
from managepro.models import (
    Archiveproduct, Category, Discount, Notification,
    Product, ProductDiscount, Report, ReportProduct,
    Users, Warehouse
)

@admin.register(Archiveproduct)
class ArchiveproductAdmin(admin.ModelAdmin):
    list_display = ('archiveid', 'productname', 'categoryid', 'quantity', 'expirydate', 'price')
    list_filter = ('categoryid', 'warehouseid')
    search_fields = ('productname', 'reason')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryid', 'categoryname')
    search_fields = ('categoryname',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discountid', 'discountpercentage', 'status')
    search_fields = ('status',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notificationid', 'productid', 'warehouseid', 'notificationtype', 'creationdate', 'status')
    list_filter = ('notificationtype', 'status')
    search_fields = ('status',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productid', 'productname', 'categoryid', 'quantity', 'price', 'expirydate', 'warehouseid')
    list_filter = ('categoryid', 'warehouseid')
    search_fields = ('productname',)


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('productid', 'discountid')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reportid', 'creationdate', 'reporttype', 'format')
    list_filter = ('reporttype', 'format')


@admin.register(ReportProduct)
class ReportProductAdmin(admin.ModelAdmin):
    list_display = ('reportid', 'productid')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'role')
    search_fields = ('username', 'role')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouseid', 'address', 'minimumstocklevel')
    search_fields = ['address']