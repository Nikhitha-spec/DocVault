from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView
from django.utils import timezone
from datetime import timedelta
from .models import User
from .forms import CustomPasswordChangeForm, ProfileUpdateForm
from activity_logs.utils import log_activity
from departments.models import Department
from documents.models import Document
from activity_logs.models import ActivityLog
from permissions_app.utils import get_accessible_documents


class CustomLoginView(LoginView):
    """
    Custom login view with activity logging.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log login activity
        log_activity(
            user=self.request.user,
            action='login',
            object_type='User',
            object_id=self.request.user.id,
            request=self.request
        )
        return response


class CustomLogoutView(LogoutView):
    """
    Custom logout view with activity logging.
    """
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            log_activity(
                user=request.user,
                action='logout',
                object_type='User',
                object_id=request.user.id,
                request=request
            )
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Custom password change view.
    """
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        log_activity(
            user=self.request.user,
            action='password_change',
            object_type='User',
            object_id=self.request.user.id,
            request=self.request
        )
        return super().form_valid(form)


@login_required
def dashboard(request):
    """
    Dashboard view based on user role.
    """
    user = request.user
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    if user.is_super_admin():
        # Super Admin Dashboard
        context = {
            'total_users': User.objects.count(),
            'total_departments': Department.objects.count(),
            'total_documents': Document.objects.filter(is_deleted=False).count(),
            'total_activities': ActivityLog.objects.filter(timestamp__date=today).count(),
            'recent_uploads': Document.objects.filter(is_deleted=False).order_by('-upload_date')[:5],
            'recent_activities': ActivityLog.objects.order_by('-timestamp')[:10],
        }
        return render(request, 'accounts/dashboard_super_admin.html', context)
    elif user.is_department_admin():
        # Department Admin Dashboard
        context = {
            'department_users': User.objects.filter(department=user.department).count(),
            'department_documents': Document.objects.filter(department=user.department, is_deleted=False).count(),
            'recent_uploads_count': Document.objects.filter(
                department=user.department, 
                is_deleted=False, 
                upload_date__gte=week_ago
            ).count(),
            'recent_activities_count': ActivityLog.objects.filter(
                user__department=user.department,
                timestamp__date=today
            ).count(),
            'department_documents_list': Document.objects.filter(
                department=user.department, 
                is_deleted=False
            ).order_by('-upload_date')[:5],
            'recent_activities': ActivityLog.objects.filter(
                user__department=user.department
            ).order_by('-timestamp')[:10],
        }
        return render(request, 'accounts/dashboard_department_admin.html', context)
    else:
        # Employee Dashboard
        accessible_docs = get_accessible_documents(user)
        context = {
            'accessible_documents': accessible_docs.count(),
            'recent_downloads': ActivityLog.objects.filter(
                user=user, 
                action='download',
                timestamp__gte=week_ago
            ).count(),
            'recent_documents': accessible_docs.filter(upload_date__gte=week_ago).count(),
            'accessible_documents_list': accessible_docs.order_by('-upload_date')[:5],
            'recent_downloads_list': ActivityLog.objects.filter(
                user=user, 
                action='download'
            ).order_by('-timestamp')[:5],
        }
        return render(request, 'accounts/dashboard_employee.html', context)


@login_required
def profile(request):
    """
    User profile view.
    """
    return render(request, 'accounts/profile.html')


class ProfileUpdateView(UpdateView):
    """
    View for updating user profile.
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        log_activity(
            user=self.request.user,
            action='update',
            object_type='User',
            object_id=self.request.user.id,
            request=self.request
        )
        return super().form_valid(form)
