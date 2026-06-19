from django.db import models
from accounts.models import User


class ActivityLog(models.Model):
    """
    Activity log model for tracking user actions.
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('upload', 'Upload'),
        ('download', 'Download'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
        ('replace', 'Replace'),
        ('version_restore', 'Version Restore'),
        ('password_change', 'Password Change'),
        ('create', 'Create'),
        ('assign_permission', 'Assign Permission'),
    ]
    
    OBJECT_TYPE_CHOICES = [
        ('User', 'User'),
        ('Department', 'Department'),
        ('Role', 'Role'),
        ('Document', 'Document'),
        ('Permission', 'Permission'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
        help_text='User who performed the action'
    )
    
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        help_text='Action performed'
    )
    
    object_type = models.CharField(
        max_length=20,
        choices=OBJECT_TYPE_CHOICES,
        help_text='Type of object affected'
    )
    
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='ID of the object affected'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Additional description of the action'
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the user'
    )
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['object_type']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{user_str} - {self.action} - {self.object_type} ({self.timestamp})"
