from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'category',
        'stock_quantity',
        'purchase_price',
        'selling_price',
        'stock_status',
        'supplier_name',
        'date_added'
    )
    list_filter = ('category', 'date_added')
    search_fields = ('name', 'sku', 'supplier_name', 'description')
    date_hierarchy = 'date_added'
    ordering = ('-date_added',)
    readonly_fields = ('date_added', 'updated_at', 'total_inventory_value', 'profit_per_unit', 'profit_margin_percent')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'category', 'description')
        }),
        ('Pricing & Stock Details', {
            'fields': (
                'purchase_price',
                'selling_price',
                'stock_quantity',
                'total_inventory_value',
                'profit_per_unit',
                'profit_margin_percent'
            )
        }),
        ('Supplier & Logistics', {
            'fields': ('supplier_name',)
        }),
        ('System Timestamps', {
            'fields': ('date_added', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
