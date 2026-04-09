from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['sku', 'name', 'price', 'cost_price', 'stock']
    readonly_fields = ['sku']
    search_fields = ['sku', 'name']