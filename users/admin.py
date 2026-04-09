from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    
    list_display = ("username", "email", "is_staff", "is_active")
    

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    

    search_fields = ("username", "first_name", "last_name", "email")