from django import forms
from .models import Role


class RoleForm(forms.ModelForm):
    """
    Form for creating and updating roles.
    """
    class Meta:
        model = Role
        fields = [
            'role_name', 'description',
            'can_create_users', 'can_edit_users', 'can_delete_users',
            'can_create_departments', 'can_edit_departments', 'can_delete_departments',
            'can_upload_documents', 'can_edit_documents', 'can_delete_documents',
            'can_manage_permissions', 'can_view_activity_logs'
        ]
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
