from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Permission
from .forms import PermissionForm
from activity_logs.utils import log_activity


def is_super_admin(user):
    """Check if user is a super admin."""
    return user.is_super_admin()


class PermissionListView(ListView):
    """
    List view for permissions.
    """
    model = Permission
    template_name = 'permissions_app/permission_list.html'
    context_object_name = 'permissions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Permission.objects.all()
        user = self.request.user
        
        # Filter based on user role
        if not user.is_super_admin():
            if user.is_department_admin():
                queryset = queryset.filter(document__department=user.department)
            elif user.is_employee():
                queryset = queryset.filter(user=user)
        
        # Filter by document
        document_id = self.request.GET.get('document', '')
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        return queryset


class PermissionCreateView(CreateView):
    """
    Create view for permissions.
    """
    model = Permission
    form_class = PermissionForm
    template_name = 'permissions_app/permission_form.html'
    success_url = reverse_lazy('permission_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Permission created successfully.')
        log_activity(
            user=self.request.user,
            action='create',
            object_type='Permission',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class PermissionDeleteView(DeleteView):
    """
    Delete view for permissions.
    """
    model = Permission
    template_name = 'permissions_app/permission_confirm_delete.html'
    success_url = reverse_lazy('permission_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_super_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        permission = self.get_object()
        messages.success(self.request, 'Permission deleted successfully.')
        log_activity(
            user=request.user,
            action='delete',
            object_type='Permission',
            object_id=permission.id,
            request=request
        )
        return super().delete(request, *args, **kwargs)


@login_required
def assign_permission(request, document_id):
    """
    Assign permission to a document.
    """
    from documents.models import Document
    document = get_object_or_404(Document, pk=document_id)
    
    # Only super admins can assign permissions
    if not request.user.is_super_admin():
        messages.error(request, "You don't have permission to assign permissions.")
        return redirect('document_detail', pk=document_id)
    
    if request.method == 'POST':
        form = PermissionForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.document = document
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'Permission assigned successfully.')
            log_activity(
                user=request.user,
                action='assign_permission',
                object_type='Permission',
                object_id=form.instance.id,
                request=request
            )
            return redirect('document_detail', pk=document_id)
    else:
        form = PermissionForm(user=request.user)
        form.fields['document'].initial = document
        form.fields['document'].widget.attrs['readonly'] = True
    
    return render(request, 'permissions_app/permission_form.html', {
        'form': form,
        'document': document
    })
