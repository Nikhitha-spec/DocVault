from django import forms
from django.core.validators import FileExtensionValidator
from .models import Document, DocumentVersion
from departments.models import Department


class DocumentForm(forms.ModelForm):
    """
    Form for creating and updating documents.
    """
    class Meta:
        model = Document
        fields = ['title', 'description', 'category', 'department', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter departments based on user role
        if user and not user.is_super_admin():
            if user.is_department_admin():
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
            elif user.is_employee():
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
                self.fields['department'].initial = user.department
                self.fields['department'].widget.attrs['readonly'] = True
    
    def clean_file(self):
        """Validate file size and type."""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 10MB.')
            
            # Check file extension
            allowed_extensions = ['pdf', 'docx', 'xlsx', 'txt']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return file


class DocumentUpdateForm(forms.ModelForm):
    """
    Form for updating document metadata (not the file).
    """
    class Meta:
        model = Document
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class DocumentReplaceForm(forms.ModelForm):
    """
    Form for replacing document file (creates new version).
    """
    class Meta:
        model = Document
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_file(self):
        """Validate file size and type."""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 10MB.')
            
            # Check file extension
            allowed_extensions = ['pdf', 'docx', 'xlsx', 'txt']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return file


class DocumentVersionForm(forms.ModelForm):
    """
    Form for creating document versions.
    """
    class Meta:
        model = DocumentVersion
        fields = ['file', 'change_notes']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'change_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_file(self):
        """Validate file size and type."""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 10MB.')
            
            # Check file extension
            allowed_extensions = ['pdf', 'docx', 'xlsx', 'txt']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return file
