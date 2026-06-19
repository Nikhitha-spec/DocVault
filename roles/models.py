from django.db import models


class Role(models.Model):
    """
    Role model for defining user roles and their permissions.
    Note: This is separate from the User.role field which is a simple choice field.
    This model allows for more granular permission management.
    """
    role_name = models.CharField(
        max_length=50,
        unique=True,
        help_text='Role name (e.g., Super Admin, Department Admin, Employee)'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Role description and permissions'
    )
    
    # Permission flags
    can_create_users = models.BooleanField(default=False)
    can_edit_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    can_create_departments = models.BooleanField(default=False)
    can_edit_departments = models.BooleanField(default=False)
    can_delete_departments = models.BooleanField(default=False)
    can_upload_documents = models.BooleanField(default=False)
    can_edit_documents = models.BooleanField(default=False)
    can_delete_documents = models.BooleanField(default=False)
    can_manage_permissions = models.BooleanField(default=False)
    can_view_activity_logs = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['role_name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.role_name
    
    @property
    def user_count(self):
        """Return the number of users with this role."""
        from accounts.models import User
        return User.objects.filter(role=self.role_name.lower().replace(' ', '_')).count()
