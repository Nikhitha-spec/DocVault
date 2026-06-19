from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import User
from departments.models import Department


class Document(models.Model):
    """
    Document model for storing file information and metadata.
    """
    CATEGORY_CHOICES = [
        ('policy', 'Policy'),
        ('report', 'Report'),
        ('contract', 'Contract'),
        ('manual', 'Manual'),
        ('invoice', 'Invoice'),
        ('presentation', 'Presentation'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text='Document title'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Document description'
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text='Document category'
    )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text='Department that owns this document'
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        help_text='User who uploaded the document'
    )
    
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'txt'])],
        help_text='Document file'
    )
    
    file_size = models.BigIntegerField(
        editable=False,
        help_text='File size in bytes'
    )
    
    file_type = models.CharField(
        max_length=10,
        editable=False,
        help_text='File extension'
    )
    
    version = models.PositiveIntegerField(
        default=1,
        help_text='Current version number'
    )
    
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    is_deleted = models.BooleanField(
        default=False,
        help_text='Soft delete flag'
    )
    
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Deletion timestamp'
    )
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category']),
            models.Index(fields=['department']),
            models.Index(fields=['upload_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Calculate file size and type before saving."""
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)
    
    def soft_delete(self):
        """Soft delete the document."""
        self.is_deleted = True
        self.deleted_at = models.timezone.now()
        self.save()
    
    def restore(self):
        """Restore a soft-deleted document."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
    
    @property
    def file_size_formatted(self):
        """Return file size in human-readable format."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    @property
    def version_count(self):
        """Return the number of versions for this document."""
        return self.versions.count()


class DocumentVersion(models.Model):
    """
    Document version model for tracking document history.
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions',
        help_text='Parent document'
    )
    
    version_number = models.PositiveIntegerField(
        help_text='Version number'
    )
    
    file = models.FileField(
        upload_to='documents/versions/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'txt'])],
        help_text='Version file'
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_versions',
        help_text='User who uploaded this version'
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    change_notes = models.TextField(
        blank=True,
        help_text='Notes about changes in this version'
    )
    
    class Meta:
        ordering = ['-version_number']
        verbose_name = 'Document Version'
        verbose_name_plural = 'Document Versions'
        unique_together = ['document', 'version_number']
    
    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
