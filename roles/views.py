from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Role
from .forms import RoleForm
from activity_logs.utils import log_activity


def is_super_admin(user):
    """Check if user is a super admin."""
    return user.is_super_admin()


class RoleListView(ListView):
    """
    List view for roles.
    """
    model = Role
    template_name = 'roles/role_list.html'
    context_object_name = 'roles'
    paginate_by = 10
    
    def get_queryset(self):
        return Role.objects.all()


class RoleCreateView(CreateView):
    """
    Create view for roles.
    """
    model = Role
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('role_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f'Role "{form.instance.role_name}" created successfully.')
        log_activity(
            user=self.request.user,
            action='create',
            object_type='Role',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class RoleUpdateView(UpdateView):
    """
    Update view for roles.
    """
    model = Role
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('role_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f'Role "{form.instance.role_name}" updated successfully.')
        log_activity(
            user=self.request.user,
            action='update',
            object_type='Role',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class RoleDeleteView(DeleteView):
    """
    Delete view for roles.
    """
    model = Role
    template_name = 'roles/role_confirm_delete.html'
    success_url = reverse_lazy('role_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        messages.success(self.request, f'Role "{role.role_name}" deleted successfully.')
        log_activity(
            user=request.user,
            action='delete',
            object_type='Role',
            object_id=role.id,
            request=request
        )
        return super().delete(request, *args, **kwargs)
