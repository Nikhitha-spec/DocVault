from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Department model.
    """
    list_display = ['name', 'description', 'created_at', 'user_count', 'document_count']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
