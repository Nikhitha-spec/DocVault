"""
Seed data script for Smart Document Management System.
Run this script to populate the database with sample data.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_dms.settings')
django.setup()

from accounts.models import User
from departments.models import Department
from roles.models import Role
from documents.models import Document, DocumentVersion
from permissions_app.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import io


def create_departments():
    """Create sample departments."""
    departments = [
        {'name': 'Human Resources', 'description': 'HR Department'},
        {'name': 'Finance', 'description': 'Finance Department'},
        {'name': 'Engineering', 'description': 'Engineering Department'},
        {'name': 'Marketing', 'description': 'Marketing Department'},
        {'name': 'Operations', 'description': 'Operations Department'},
    ]
    
    for dept_data in departments:
        Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
    
    print("✓ Departments created")


def create_roles():
    """Create sample roles."""
    roles = [
        {
            'role_name': 'Super Admin',
            'description': 'Full system access',
            'can_create_users': True,
            'can_edit_users': True,
            'can_delete_users': True,
            'can_create_departments': True,
            'can_edit_departments': True,
            'can_delete_departments': True,
            'can_upload_documents': True,
            'can_edit_documents': True,
            'can_delete_documents': True,
            'can_manage_permissions': True,
            'can_view_activity_logs': True,
        },
        {
            'role_name': 'Department Admin',
            'description': 'Department-level access',
            'can_create_users': False,
            'can_edit_users': False,
            'can_delete_users': False,
            'can_create_departments': False,
            'can_edit_departments': False,
            'can_delete_departments': False,
            'can_upload_documents': True,
            'can_edit_documents': True,
            'can_delete_documents': False,
            'can_manage_permissions': False,
            'can_view_activity_logs': True,
        },
        {
            'role_name': 'Employee',
            'description': 'Basic employee access',
            'can_create_users': False,
            'can_edit_users': False,
            'can_delete_users': False,
            'can_create_departments': False,
            'can_edit_departments': False,
            'can_delete_departments': False,
            'can_upload_documents': False,
            'can_edit_documents': False,
            'can_delete_documents': False,
            'can_manage_permissions': False,
            'can_view_activity_logs': False,
        },
    ]
    
    for role_data in roles:
        Role.objects.get_or_create(
            role_name=role_data['role_name'],
            defaults=role_data
        )
    
    print("✓ Roles created")


def create_users():
    """Create sample users."""
    hr_dept = Department.objects.get(name='Human Resources')
    finance_dept = Department.objects.get(name='Finance')
    engineering_dept = Department.objects.get(name='Engineering')
    
    users = [
        {
            'username': 'admin',
            'email': 'admin@smartdms.com',
            'first_name': 'Super',
            'last_name': 'Admin',
            'password': 'admin123',
            'role': 'super_admin',
            'department': None,
            'is_superuser': True,
            'is_staff': True,
        },
        {
            'username': 'hr_admin',
            'email': 'hr.admin@smartdms.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': 'hr123',
            'role': 'department_admin',
            'department': hr_dept,
            'is_superuser': False,
            'is_staff': True,
        },
        {
            'username': 'finance_admin',
            'email': 'finance.admin@smartdms.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'finance123',
            'role': 'department_admin',
            'department': finance_dept,
            'is_superuser': False,
            'is_staff': True,
        },
        {
            'username': 'engineer1',
            'email': 'engineer1@smartdms.com',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'password': 'engineer123',
            'role': 'employee',
            'department': engineering_dept,
            'is_superuser': False,
            'is_staff': False,
        },
        {
            'username': 'engineer2',
            'email': 'engineer2@smartdms.com',
            'first_name': 'Alice',
            'last_name': 'Williams',
            'password': 'engineer123',
            'role': 'employee',
            'department': engineering_dept,
            'is_superuser': False,
            'is_staff': False,
        },
        {
            'username': 'hr_employee',
            'email': 'hr.employee@smartdms.com',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'password': 'hr123',
            'role': 'employee',
            'department': hr_dept,
            'is_superuser': False,
            'is_staff': False,
        },
    ]
    
    for user_data in users:
        password = user_data.pop('password')
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password(password)
            user.save()
    
    print("✓ Users created")


def create_documents():
    """Create sample documents."""
    hr_dept = Department.objects.get(name='Human Resources')
    finance_dept = Department.objects.get(name='Finance')
    engineering_dept = Department.objects.get(name='Engineering')
    
    admin_user = User.objects.get(username='admin')
    hr_admin = User.objects.get(username='hr_admin')
    finance_admin = User.objects.get(username='finance_admin')
    
    # Create sample text files
    sample_content = b"This is a sample document content for testing purposes."
    
    documents = [
        {
            'title': 'Employee Handbook 2024',
            'description': 'Company employee handbook with policies and procedures',
            'category': 'policy',
            'department': hr_dept,
            'uploaded_by': hr_admin,
            'file': SimpleUploadedFile("employee_handbook.txt", sample_content),
        },
        {
            'title': 'Financial Report Q1 2024',
            'description': 'First quarter financial report',
            'category': 'report',
            'department': finance_dept,
            'uploaded_by': finance_admin,
            'file': SimpleUploadedFile("financial_report_q1.txt", sample_content),
        },
        {
            'title': 'Project Specifications',
            'description': 'Technical specifications for the new project',
            'category': 'manual',
            'department': engineering_dept,
            'uploaded_by': admin_user,
            'file': SimpleUploadedFile("project_specs.txt", sample_content),
        },
        {
            'title': 'Company Policies',
            'description': 'General company policies document',
            'category': 'policy',
            'department': hr_dept,
            'uploaded_by': hr_admin,
            'file': SimpleUploadedFile("company_policies.txt", sample_content),
        },
        {
            'title': 'Budget Plan 2024',
            'description': 'Annual budget plan for the company',
            'category': 'report',
            'department': finance_dept,
            'uploaded_by': finance_admin,
            'file': SimpleUploadedFile("budget_plan.txt", sample_content),
        },
    ]
    
    for doc_data in documents:
        Document.objects.get_or_create(
            title=doc_data['title'],
            defaults=doc_data
        )
    
    print("✓ Documents created")


def create_permissions():
    """Create sample permissions."""
    engineering_dept = Department.objects.get(name='Engineering')
    engineer1 = User.objects.get(username='engineer1')
    engineer2 = User.objects.get(username='engineer2')
    
    # Get documents
    project_specs = Document.objects.get(title='Project Specifications')
    
    # Give engineering employees access to project specs
    Permission.objects.get_or_create(
        document=project_specs,
        department=engineering_dept,
        defaults={
            'can_view': True,
            'can_download': True,
            'can_edit': False,
            'can_delete': False,
            'created_by': User.objects.get(username='admin')
        }
    )
    
    # Give specific user permission
    Permission.objects.get_or_create(
        document=project_specs,
        user=engineer1,
        defaults={
            'can_view': True,
            'can_download': True,
            'can_edit': True,
            'can_delete': False,
            'created_by': User.objects.get(username='admin')
        }
    )
    
    print("✓ Permissions created")


def create_activity_logs():
    """Create sample activity logs."""
    from activity_logs.models import ActivityLog
    from django.utils import timezone
    from datetime import timedelta
    
    admin_user = User.objects.get(username='admin')
    hr_admin = User.objects.get(username='hr_admin')
    finance_admin = User.objects.get(username='finance_admin')
    engineer1 = User.objects.get(username='engineer1')
    
    # Create sample activity logs
    activities = [
        {
            'user': admin_user,
            'action': 'create',
            'object_type': 'Department',
            'object_id': Department.objects.get(name='Human Resources').id,
            'description': 'Created Human Resources department',
            'ip_address': '127.0.0.1',
        },
        {
            'user': admin_user,
            'action': 'create',
            'object_type': 'Role',
            'object_id': Role.objects.get(role_name='Super Admin').id,
            'description': 'Created Super Admin role',
            'ip_address': '127.0.0.1',
        },
        {
            'user': hr_admin,
            'action': 'upload',
            'object_type': 'Document',
            'object_id': Document.objects.get(title='Employee Handbook 2024').id,
            'description': 'Uploaded Employee Handbook 2024',
            'ip_address': '127.0.0.1',
        },
        {
            'user': finance_admin,
            'action': 'upload',
            'object_type': 'Document',
            'object_id': Document.objects.get(title='Financial Report Q1 2024').id,
            'description': 'Uploaded Financial Report Q1 2024',
            'ip_address': '127.0.0.1',
        },
        {
            'user': engineer1,
            'action': 'download',
            'object_type': 'Document',
            'object_id': Document.objects.get(title='Project Specifications').id,
            'description': 'Downloaded Project Specifications',
            'ip_address': '127.0.0.1',
        },
        {
            'user': admin_user,
            'action': 'assign_permission',
            'object_type': 'Permission',
            'description': 'Assigned permissions to Engineering department',
            'ip_address': '127.0.0.1',
        },
        {
            'user': hr_admin,
            'action': 'update',
            'object_type': 'Document',
            'object_id': Document.objects.get(title='Employee Handbook 2024').id,
            'description': 'Updated Employee Handbook 2024',
            'ip_address': '127.0.0.1',
        },
    ]
    
    for activity_data in activities:
        ActivityLog.objects.get_or_create(
            user=activity_data['user'],
            action=activity_data['action'],
            object_type=activity_data['object_type'],
            object_id=activity_data.get('object_id'),
            description=activity_data['description'],
            ip_address=activity_data['ip_address'],
            defaults={'timestamp': timezone.now() - timedelta(hours=len(activities) - activities.index(activity_data))}
        )
    
    print("✓ Activity logs created")


def seed_all():
    """Run all seed functions."""
    print("Seeding database...")
    print("-" * 50)
    
    create_departments()
    create_roles()
    create_users()
    create_documents()
    create_permissions()
    create_activity_logs()
    
    print("-" * 50)
    print("✓ Database seeded successfully!")
    print("\nLogin credentials:")
    print("  Super Admin: admin / admin123")
    print("  HR Admin: hr_admin / hr123")
    print("  Finance Admin: finance_admin / finance123")
    print("  Engineer: engineer1 / engineer123")


if __name__ == '__main__':
    seed_all()
