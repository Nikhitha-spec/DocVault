from rest_framework import serializers
from accounts.models import User
from departments.models import Department
from documents.models import Document, DocumentVersion
from permissions_app.models import Permission
from activity_logs.models import ActivityLog


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'department', 'department_name', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'role', 'department']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    user_count = serializers.ReadOnlyField()
    document_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at', 'user_count', 'document_count']
        read_only_fields = ['id', 'created_at']


class DocumentVersionSerializer(serializers.ModelSerializer):
    """Serializer for DocumentVersion model."""
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = ['id', 'version_number', 'file', 'uploaded_by', 'uploaded_by_username', 'uploaded_at', 'change_notes']
        read_only_fields = ['id', 'uploaded_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    file_size_formatted = serializers.ReadOnlyField()
    version_count = serializers.ReadOnlyField()
    versions = DocumentVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'category', 'department', 'department_name', 'uploaded_by', 'uploaded_by_username', 'file', 'file_size', 'file_size_formatted', 'file_type', 'version', 'version_count', 'upload_date', 'last_modified', 'is_deleted', 'deleted_at', 'versions']
        read_only_fields = ['id', 'file_size', 'file_type', 'version', 'upload_date', 'last_modified', 'deleted_at']


class DocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating documents."""
    class Meta:
        model = Document
        fields = ['title', 'description', 'category', 'department', 'file']


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""
    document_title = serializers.CharField(source='document.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'document', 'document_title', 'user', 'user_username', 'role', 'department', 'department_name', 'can_view', 'can_download', 'can_edit', 'can_delete', 'created_at', 'created_by', 'created_by_username']
        read_only_fields = ['id', 'created_at', 'created_by']


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'user_username', 'action', 'object_type', 'object_id', 'description', 'timestamp', 'ip_address']
        read_only_fields = ['id', 'timestamp']
