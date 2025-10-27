from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'is_carton', 'carton_count', 'pairs_per_carton', 'show_amount']
    readonly_fields = ['show_amount']

    def show_amount(self, obj):
        if obj.id:
            return f"{obj.item_amount():,} تومان"
        return "---"
    show_amount.short_description = "مبلغ آیتم"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'short_address', 'created_at']
    search_fields = ['name', 'phone']
    list_filter = ['created_at']
    
    def short_address(self, obj):
        return obj.address[:50] + "..." if len(obj.address) > 50 else obj.address
    short_address.short_description = "آدرس"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'color', 'price', 'stock', 'show_price']
    list_filter = ['size', 'color']
    search_fields = ['name']
    
    def show_price(self, obj):
        return f"{obj.price:,} تومان"
    show_price.short_description = "قیمت"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'status', 'is_invoice', 'product_count', 'total_amount', 'total_pairs']
    list_filter = ['status', 'is_invoice', 'order_date']
    search_fields = ['customer__name']
    list_editable = ['status', 'is_invoice']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('customer', 'status', 'is_invoice')
        }),
        ('یادداشت', {
            'fields': ('notes',)
        }),
    )
    
    def product_count(self, obj):
        return obj.order_items.count()
    product_count.short_description = "تعداد محصولات"
    
    def total_amount(self, obj):
        return f"{obj.total_amount():,} تومان"
    total_amount.short_description = "مبلغ کل"
    
    def total_pairs(self, obj):
        return f"{obj.total_pairs():,} جفت"
    total_pairs.short_description = "تعداد کل جفت"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'show_quantity', 'is_carton', 'item_amount']
    list_filter = ['is_carton', 'product__size']
    
    def show_quantity(self, obj):
        if obj.is_carton:
            return f"{obj.carton_count} کارتن ({obj.pairs_per_carton} جفت در هر کارتن)"
        return f"{obj.quantity} جفت"
    show_quantity.short_description = "مقدار سفارش"
    
    def item_amount(self, obj):
        return f"{obj.item_amount():,} تومان"
    item_amount.short_description = "مبلغ آیتم"