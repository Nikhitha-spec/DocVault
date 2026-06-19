from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active', 'created_at']
    list_filter = ['role', 'department', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'department', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'role', 'department')
        }),
    )
