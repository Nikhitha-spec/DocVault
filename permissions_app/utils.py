from django.db.models import Q
from .models import Permission


def has_document_permission(user, document, permission_type='view'):
    """
    Check if a user has permission to access a document.
    
    Args:
        user: The user object
        document: The document object
        permission_type: Type of permission to check (view, download, edit, delete)
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    # Super admins have access to everything
    if user.is_super_admin():
        return True
    
    # Department admins can access documents in their department
    if user.is_department_admin() and user.department == document.department:
        if permission_type in ['view', 'download']:
            return True
        elif permission_type in ['edit', 'delete']:
            # Department admins can edit but not delete
            return permission_type == 'edit'
    
    # Check for explicit permissions
    permission_field = f'can_{permission_type}'
    
    # Check user-specific permission
    user_permission = Permission.objects.filter(
        document=document,
        user=user
    ).first()
    
    if user_permission:
        return getattr(user_permission, permission_field, False)
    
    # Check department-based permission
    if user.department:
        dept_permission = Permission.objects.filter(
            document=document,
            department=user.department
        ).first()
        
        if dept_permission:
            return getattr(dept_permission, permission_field, False)
    
    # Check role-based permission
    role_permission = Permission.objects.filter(
        document=document,
        role=user.role
    ).first()
    
    if role_permission:
        return getattr(role_permission, permission_field, False)
    
    return False


def get_accessible_documents(user):
    """
    Get all documents a user can access.
    
    Args:
        user: The user object
    
    Returns:
        QuerySet: Accessible documents
    """
    from documents.models import Document
    
    # Super admins see all documents
    if user.is_super_admin():
        return Document.objects.filter(is_deleted=False)
    
    # Department admins see their department's documents
    if user.is_department_admin():
        return Document.objects.filter(department=user.department, is_deleted=False)
    
    # Employees see documents they have explicit permission to access
    accessible_doc_ids = Permission.objects.filter(
        Q(user=user) | Q(department=user.department) | Q(role=user.role),
        can_view=True
    ).values_list('document_id', flat=True)
    
    return Document.objects.filter(id__in=accessible_doc_ids, is_deleted=False)
