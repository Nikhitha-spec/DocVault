from django.contrib.auth.models import AbstractUser
from django.db import models
from departments.models import Department


class User(AbstractUser):
    """
    Custom User model with role and department fields.
    Extends Django's AbstractUser to add custom fields.
    """
    
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('department_admin', 'Department Admin'),
        ('employee', 'Employee'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        help_text='User role in the system'
    )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text='Department the user belongs to'
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text='User profile picture'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = super().get_full_name()
        return full_name if full_name else self.username
    
    def is_super_admin(self):
        """Check if user is a super admin."""
        return self.role == 'super_admin' or self.is_superuser
    
    def is_department_admin(self):
        """Check if user is a department admin."""
        return self.role == 'department_admin'
    
    def is_employee(self):
        """Check if user is an employee."""
        return self.role == 'employee'
