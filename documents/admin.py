from django.contrib import admin
from .models import Document, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin interface for Document model.
    """
    list_display = ['title', 'category', 'department', 'uploaded_by', 'file_type', 'file_size_formatted', 'version', 'is_deleted', 'upload_date']
    list_filter = ['category', 'department', 'file_type', 'is_deleted', 'upload_date']
    search_fields = ['title', 'description']
    ordering = ['-upload_date']
    readonly_fields = ['file_size', 'file_type', 'upload_date', 'last_modified', 'deleted_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'department', 'uploaded_by', 'file')
        }),
        ('File Information', {
            'fields': ('file_size', 'file_type', 'version')
        }),
        ('Timestamps', {
            'fields': ('upload_date', 'last_modified')
        }),
        ('Deletion', {
            'fields': ('is_deleted', 'deleted_at')
        }),
    )


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    """
    Admin interface for DocumentVersion model.
    """
    list_display = ['document', 'version_number', 'uploaded_by', 'uploaded_at']
    list_filter = ['version_number', 'uploaded_at']
    search_fields = ['document__title', 'change_notes']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at']
