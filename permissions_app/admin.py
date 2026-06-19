from django.contrib import admin
from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin interface for Permission model.
    """
    list_display = ['document', 'user', 'role', 'department', 'can_view', 'can_download', 'can_edit', 'can_delete', 'created_at']
    list_filter = ['role', 'department', 'can_view', 'can_download', 'can_edit', 'can_delete', 'created_at']
    search_fields = ['document__title', 'user__username', 'role', 'department__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'created_by']
    
    fieldsets = (
        (None, {
            'fields': ('document', 'user', 'role', 'department')
        }),
        ('Permissions', {
            'fields': ('can_view', 'can_download', 'can_edit', 'can_delete')
        }),
        ('Metadata', {
            'fields': ('created_at', 'created_by')
        }),
    )
