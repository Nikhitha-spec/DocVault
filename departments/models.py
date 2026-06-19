from django.db import models


class Department(models.Model):
    """
    Department model for organizing users and documents.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Department name'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Department description'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return self.name
    
    @property
    def user_count(self):
        """Return the number of users in this department."""
        return self.users.count()
    
    @property
    def document_count(self):
        """Return the number of documents in this department."""
        return self.documents.count()
