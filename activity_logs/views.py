from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
from django.db.models import Q
from django.utils.decorators import method_decorator
from .models import ActivityLog


def is_super_admin(user):
    """Check if user is a super admin."""
    return user.is_super_admin()


def is_department_admin(user):
    """Check if user is a department admin."""
    return user.is_department_admin()


class ActivityLogListView(ListView):
    """
    List view for activity logs.
    """
    model = ActivityLog
    template_name = 'activity_logs/activity_log_list.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_super_admin() or u.is_department_admin()))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = ActivityLog.objects.all()
        user = self.request.user
        
        # Department admins only see logs related to their department
        if user.is_department_admin():
            from accounts.models import User
            dept_users = User.objects.filter(department=user.department)
            queryset = queryset.filter(user__in=dept_users)
        
        # Filter by action
        action = self.request.GET.get('action', '')
        if action:
            queryset = queryset.filter(action=action)
        
        # Filter by object type
        object_type = self.request.GET.get('object_type', '')
        if object_type:
            queryset = queryset.filter(object_type=object_type)
        
        # Filter by user
        user_id = self.request.GET.get('user', '')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(user__username__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = self.request.GET.get('action', '')
        context['object_type'] = self.request.GET.get('object_type', '')
        context['user'] = self.request.GET.get('user', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        if self.request.user.is_super_admin():
            from accounts.models import User
            context['users'] = User.objects.all()
        
        return context
