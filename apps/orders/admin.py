from django.contrib import admin
from apps.orders.models import Cart, CartItem, Order, OrderItem, Invoice


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'session_key', 'total_items', 'total', 'updated_at']
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    search_fields = ['order_number', 'user__username', 'phone']
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'order', 'issued_date', 'due_date', 'total']
    search_fields = ['invoice_number', 'order__order_number']
