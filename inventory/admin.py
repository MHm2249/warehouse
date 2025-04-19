from django.contrib import admin
from .models import Product, Warehouse, Transaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'barcode')



@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'last_updated')
    list_filter = ('product__category',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'transaction_type', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')