from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Department
from .forms import DepartmentForm
from activity_logs.utils import log_activity


def is_super_admin(user):
    """Check if user is a super admin."""
    return user.is_super_admin()


class DepartmentListView(ListView):
    """
    List view for departments.
    """
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10
    
    def get_queryset(self):
        return Department.objects.all()


class DepartmentCreateView(CreateView):
    """
    Create view for departments.
    """
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f'Department "{form.instance.name}" created successfully.')
        log_activity(
            user=self.request.user,
            action='create',
            object_type='Department',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class DepartmentUpdateView(UpdateView):
    """
    Update view for departments.
    """
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f'Department "{form.instance.name}" updated successfully.')
        log_activity(
            user=self.request.user,
            action='update',
            object_type='Department',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class DepartmentDeleteView(DeleteView):
    """
    Delete view for departments.
    """
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        messages.success(self.request, f'Department "{department.name}" deleted successfully.')
        log_activity(
            user=request.user,
            action='delete',
            object_type='Department',
            object_id=department.id,
            request=request
        )
        return super().delete(request, *args, **kwargs)
