from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin interface for Role model.
    """
    list_display = ['role_name', 'description', 'can_upload_documents', 'can_manage_permissions', 'created_at']
    search_fields = ['role_name', 'description']
    ordering = ['role_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('role_name', 'description')
        }),
        ('User Management Permissions', {
            'fields': ('can_create_users', 'can_edit_users', 'can_delete_users')
        }),
        ('Department Management Permissions', {
            'fields': ('can_create_departments', 'can_edit_departments', 'can_delete_departments')
        }),
        ('Document Management Permissions', {
            'fields': ('can_upload_documents', 'can_edit_documents', 'can_delete_documents')
        }),
        ('System Permissions', {
            'fields': ('can_manage_permissions', 'can_view_activity_logs')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
