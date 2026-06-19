from django.db import models
from accounts.models import User
from departments.models import Department
from documents.models import Document


class Permission(models.Model):
    """
    Permission model for controlling document access.
    Supports role-based, department-based, and user-specific permissions.
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions',
        help_text='Document this permission applies to'
    )
    
    # At least one of these should be set
    role = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Role that has access (e.g., super_admin, department_admin, employee)'
    )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='permissions',
        help_text='Department that has access'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='permissions',
        help_text='Specific user that has access'
    )
    
    can_view = models.BooleanField(default=True, help_text='Can view the document')
    can_download = models.BooleanField(default=True, help_text='Can download the document')
    can_edit = models.BooleanField(default=False, help_text='Can edit the document')
    can_delete = models.BooleanField(default=False, help_text='Can delete the document')
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_permissions',
        help_text='User who created this permission'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        unique_together = [['document', 'role', 'department', 'user']]
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.document.title}"
        elif self.department:
            return f"{self.department.name} - {self.document.title}"
        elif self.role:
            return f"{self.role} - {self.document.title}"
        return f"Permission - {self.document.title}"
    
    def clean(self):
        """Ensure at least one of role, department, or user is set."""
        from django.core.exceptions import ValidationError
        if not self.role and not self.department and not self.user:
            raise ValidationError("At least one of role, department, or user must be set.")
