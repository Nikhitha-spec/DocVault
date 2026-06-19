from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    Admin interface for ActivityLog model.
    """
    list_display = ['user', 'action', 'object_type', 'object_id', 'ip_address', 'timestamp']
    list_filter = ['action', 'object_type', 'timestamp']
    search_fields = ['user__username', 'description']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'action', 'object_type', 'object_id', 'description')
        }),
        ('Metadata', {
            'fields': ('timestamp', 'ip_address')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual addition of activity logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing of activity logs."""
        return False
