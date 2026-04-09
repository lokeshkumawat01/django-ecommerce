from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.admin import TabularInline
from .models import Order, OrderItem, Address

# Inline Setup
class OrderItemInline(TabularInline): # Unfold ka TabularInline
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

# Main Admin Setup
@admin.register(Order)
class OrderAdmin(ModelAdmin): # 🔥 admin.ModelAdmin ki jagah Unfold ka ModelAdmin
    list_display = ['order_id', 'user', 'total_amount', 'status', 'is_paid', 'tracking_number']
    list_editable = ['status', 'is_paid']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['order_id', 'user__username', 'tracking_number']
    readonly_fields = ['order_id']
    inlines = [OrderItemInline]


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'city']
