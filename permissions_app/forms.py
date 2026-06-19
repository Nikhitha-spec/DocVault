from django import forms
from .models import Permission
from documents.models import Document
from accounts.models import User
from departments.models import Department


class PermissionForm(forms.ModelForm):
    """
    Form for creating and updating permissions.
    """
    class Meta:
        model = Permission
        fields = ['document', 'user', 'role', 'department', 'can_view', 'can_download', 'can_edit', 'can_delete']
        widgets = {
            'document': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'can_view': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_download': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter documents based on user role
        if user and not user.is_super_admin():
            if user.is_department_admin():
                self.fields['document'].queryset = Document.objects.filter(department=user.department, is_deleted=False)
            elif user.is_employee():
                self.fields['document'].queryset = Document.objects.filter(department=user.department, is_deleted=False)
        
        # Filter users
        if user and not user.is_super_admin():
            if user.is_department_admin():
                self.fields['user'].queryset = User.objects.filter(department=user.department)
        
        # Filter departments
        if user and not user.is_super_admin():
            if user.is_department_admin():
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
    
    def clean(self):
        """Ensure at least one of role, department, or user is set."""
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        department = cleaned_data.get('department')
        user = cleaned_data.get('user')
        
        if not role and not department and not user:
            raise forms.ValidationError("At least one of role, department, or user must be set.")
        
        return cleaned_data
