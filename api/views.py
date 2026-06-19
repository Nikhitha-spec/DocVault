from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from accounts.models import User
from departments.models import Department
from documents.models import Document, DocumentVersion
from permissions_app.models import Permission
from activity_logs.models import ActivityLog
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    DepartmentSerializer,
    DocumentSerializer,
    DocumentCreateSerializer,
    DocumentVersionSerializer,
    PermissionSerializer,
    ActivityLogSerializer,
)
from permissions_app.utils import has_document_permission, get_accessible_documents


class LoginAPIView(APIView):
    """API view for user login."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutAPIView(APIView):
    """API view for user logout."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'})
        except Exception:
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role', 'department']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return User.objects.all()
        elif user.is_department_admin():
            return User.objects.filter(department=user.department)
        else:
            return User.objects.filter(id=user.id)
    
    def perform_create(self, serializer):
        serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='create',
            object_type='User',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_update(self, serializer):
        serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='update',
            object_type='User',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action='delete',
            object_type='User',
            object_id=instance.id,
            ip_address=self.get_client_ip(self.request)
        )
        instance.delete()
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Department.objects.all()
        elif user.is_department_admin():
            return Department.objects.filter(id=user.department.id)
        else:
            return Department.objects.filter(id=user.department.id)
    
    def perform_create(self, serializer):
        serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='create',
            object_type='Department',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_update(self, serializer):
        serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='update',
            object_type='Department',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action='delete',
            object_type='Department',
            object_id=instance.id,
            ip_address=self.get_client_ip(self.request)
        )
        instance.delete()
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document model."""
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['category', 'department', 'file_type']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'upload_date', 'last_modified']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Document.objects.filter(is_deleted=False)
        elif user.is_department_admin():
            return Document.objects.filter(department=user.department, is_deleted=False)
        else:
            return get_accessible_documents(user)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action='upload',
            object_type='Document',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_update(self, serializer):
        serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='update',
            object_type='Document',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_destroy(self, instance):
        instance.soft_delete()
        ActivityLog.objects.create(
            user=self.request.user,
            action='delete',
            object_type='Document',
            object_id=instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Download a document."""
        document = self.get_object()
        
        if not has_document_permission(request.user, document, 'download'):
            return Response(
                {'error': 'You do not have permission to download this document.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        ActivityLog.objects.create(
            user=request.user,
            action='download',
            object_type='Document',
            object_id=document.id,
            ip_address=self.get_client_ip(request)
        )
        
        return Response({
            'message': 'Download logged successfully.',
            'file_url': document.file.url
        })
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted document."""
        if not request.user.is_super_admin():
            return Response(
                {'error': 'Only super admins can restore documents.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        document = self.get_object()
        document.restore()
        
        ActivityLog.objects.create(
            user=request.user,
            action='restore',
            object_type='Document',
            object_id=document.id,
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'message': 'Document restored successfully.'})
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Permission model."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['document', 'role', 'department', 'user']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Permission.objects.all()
        elif user.is_department_admin():
            return Permission.objects.filter(document__department=user.department)
        else:
            return Permission.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action='assign_permission',
            object_type='Permission',
            object_id=serializer.instance.id,
            ip_address=self.get_client_ip(self.request)
        )
    
    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action='delete',
            object_type='Permission',
            object_id=instance.id,
            ip_address=self.get_client_ip(self.request)
        )
        instance.delete()
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ActivityLog model (read-only)."""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['action', 'object_type', 'user']
    search_fields = ['description']
    ordering_fields = ['timestamp']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return ActivityLog.objects.all()
        elif user.is_department_admin():
            from accounts.models import User
            dept_users = User.objects.filter(department=user.department)
            return ActivityLog.objects.filter(user__in=dept_users)
        else:
            return ActivityLog.objects.filter(user=user)
