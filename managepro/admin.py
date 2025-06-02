from django.contrib import admin
from .models import *

# Inline для связей Report → ReportProduct
class ReportProductInline(admin.TabularInline):
    model = ReportProduct
    extra = 0

# Inline для Product → ProductDiscount
class ProductDiscountInline(admin.TabularInline):
    model = ProductDiscount
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryid', 'categoryname')
    search_fields = ('categoryname',)
    list_display_links = ('categoryname',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productid', 'productname', 'category_name', 'quantity', 'price', 'datereceived')
    search_fields = ('productname',)
    list_filter = ('categoryid', 'warehouseid')
    inlines = [ProductDiscountInline]
    raw_id_fields = ('categoryid', 'warehouseid')
    readonly_fields = ('productid',)
    list_display_links = ('productname',)
    date_hierarchy = 'expirydate'

    @admin.display(description='Category')
    def category_name(self, obj):
        return obj.categoryid.categoryname if obj.categoryid else '-'


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouseid', 'address', 'minimumstocklevel')
    search_fields = ('address',)
    list_display_links = ('address',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discountid', 'discountpercentage', 'is_active')
    list_filter = ('status',)
    search_fields = ('status',)

    @admin.display(boolean=True, description='Active?')
    def is_active(self, obj):
        return obj.status == 'active'


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('productid', 'discountid')
    raw_id_fields = ('productid', 'discountid')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reportid', 'reporttype', 'creationdate')
    inlines = [ReportProductInline]
    date_hierarchy = 'creationdate'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notificationid', 'productid', 'warehouseid', 'notificationtype', 'creationdate', 'status')
    list_filter = ('notificationtype', 'status')
    date_hierarchy = 'creationdate'


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'role')
    search_fields = ('username', 'role')
    readonly_fields = ('userid',)
