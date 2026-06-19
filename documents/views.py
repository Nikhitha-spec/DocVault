from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import FileResponse, Http404
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Document, DocumentVersion
from .forms import DocumentForm, DocumentUpdateForm, DocumentReplaceForm, DocumentVersionForm
from permissions_app.utils import has_document_permission
from activity_logs.utils import log_activity


class DocumentListView(ListView):
    """
    List view for documents with search and filtering.
    """
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_deleted=False)
        user = self.request.user
        
        # Filter based on user permissions
        if not user.is_super_admin():
            if user.is_department_admin():
                queryset = queryset.filter(department=user.department)
            elif user.is_employee():
                # Employees can only see documents they have permission to access
                from permissions_app.models import Permission
                accessible_docs = Permission.objects.filter(
                    Q(user=user) | Q(department=user.department) | Q(role=user.role)
                ).values_list('document_id', flat=True)
                queryset = queryset.filter(id__in=accessible_docs)
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by category
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by department
        department = self.request.GET.get('department', '')
        if department:
            queryset = queryset.filter(department_id=department)
        
        # Filter by file type
        file_type = self.request.GET.get('file_type', '')
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-upload_date')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['category'] = self.request.GET.get('category', '')
        context['department'] = self.request.GET.get('department', '')
        context['file_type'] = self.request.GET.get('file_type', '')
        context['sort_by'] = self.request.GET.get('sort', '-upload_date')
        
        from departments.models import Department
        context['departments'] = Department.objects.all()
        
        return context


class DocumentDetailView(DetailView):
    """
    Detail view for a document.
    """
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_deleted=False)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = self.get_object()
        
        # Check permission
        if not has_document_permission(self.request.user, document):
            raise Http404("You don't have permission to view this document.")
        
        context['versions'] = document.versions.all()
        context['can_edit'] = self.request.user.is_super_admin() or (
            self.request.user.is_department_admin() and 
            self.request.user.department == document.department
        )
        context['can_delete'] = self.request.user.is_super_admin()
        
        return context


class DocumentCreateView(CreateView):
    """
    Create view for documents.
    """
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('document_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Only super admins and department admins can upload
        if not (self.request.user.is_super_admin() or self.request.user.is_department_admin()):
            messages.error(self.request, "You don't have permission to upload documents.")
            return redirect('document_list')
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, f'Document "{form.instance.title}" uploaded successfully.')
        log_activity(
            user=self.request.user,
            action='upload',
            object_type='Document',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class DocumentUpdateView(UpdateView):
    """
    Update view for document metadata.
    """
    model = Document
    form_class = DocumentUpdateForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('document_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        document = self.get_object()
        # Check permission
        if not (self.request.user.is_super_admin() or 
                (self.request.user.is_department_admin() and 
                 self.request.user.department == document.department)):
            messages.error(self.request, "You don't have permission to edit this document.")
            return redirect('document_detail', pk=document.pk)
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f'Document "{form.instance.title}" updated successfully.')
        log_activity(
            user=self.request.user,
            action='update',
            object_type='Document',
            object_id=form.instance.id,
            request=self.request
        )
        return super().form_valid(form)


class DocumentDeleteView(DeleteView):
    """
    Delete view for documents (soft delete).
    """
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('document_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Only super admins can delete
        if not self.request.user.is_super_admin():
            messages.error(self.request, "You don't have permission to delete documents.")
            return redirect('document_detail', pk=self.kwargs['pk'])
        return super().dispatch(*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        document.soft_delete()
        messages.success(self.request, f'Document "{document.title}" deleted successfully.')
        log_activity(
            user=request.user,
            action='delete',
            object_type='Document',
            object_id=document.id,
            request=request
        )
        return redirect(self.success_url)


@login_required
def document_download(request, pk):
    """
    Download a document.
    """
    document = get_object_or_404(Document, pk=pk, is_deleted=False)
    
    # Check permission
    if not has_document_permission(request.user, document):
        raise Http404("You don't have permission to download this document.")
    
    # Log download
    log_activity(
        user=request.user,
        action='download',
        object_type='Document',
        object_id=document.id,
        request=request
    )
    
    try:
        response = FileResponse(document.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{document.title}.{document.file_type}"'
        return response
    except FileNotFoundError:
        raise Http404("File not found.")


@login_required
def document_preview(request, pk):
    """
    Preview a PDF document.
    """
    document = get_object_or_404(Document, pk=pk, is_deleted=False)
    
    # Check permission
    if not has_document_permission(request.user, document):
        raise Http404("You don't have permission to view this document.")
    
    if document.file_type != 'pdf':
        messages.error(request, "Only PDF files can be previewed.")
        return redirect('document_detail', pk=pk)
    
    return render(request, 'documents/document_preview.html', {'document': document})


@login_required
def document_replace(request, pk):
    """
    Replace document file (creates new version).
    """
    document = get_object_or_404(Document, pk=pk, is_deleted=False)
    
    # Check permission
    if not (request.user.is_super_admin() or 
            (request.user.is_department_admin() and 
             request.user.department == document.department)):
        messages.error(request, "You don't have permission to replace this document.")
        return redirect('document_detail', pk=pk)
    
    if request.method == 'POST':
        form = DocumentReplaceForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            # Create new version
            new_version_number = document.version + 1
            DocumentVersion.objects.create(
                document=document,
                version_number=new_version_number,
                file=document.file,
                uploaded_by=request.user,
                change_notes="Previous version before replacement"
            )
            
            # Update document
            document.version = new_version_number
            form.save()
            
            messages.success(request, f'Document "{document.title}" replaced successfully. New version: {new_version_number}')
            log_activity(
                user=request.user,
                action='replace',
                object_type='Document',
                object_id=document.id,
                request=request
            )
            return redirect('document_detail', pk=pk)
    else:
        form = DocumentReplaceForm(instance=document)
    
    return render(request, 'documents/document_replace.html', {'form': form, 'document': document})


@login_required
def document_restore(request, pk):
    """
    Restore a soft-deleted document.
    """
    document = get_object_or_404(Document, pk=pk, is_deleted=True)
    
    # Only super admins can restore
    if not request.user.is_super_admin():
        messages.error(request, "You don't have permission to restore documents.")
        return redirect('document_list')
    
    document.restore()
    messages.success(request, f'Document "{document.title}" restored successfully.')
    log_activity(
        user=request.user,
        action='restore',
        object_type='Document',
        object_id=document.id,
        request=request
    )
    
    return redirect('document_list')


@login_required
def document_version_detail(request, pk, version_number):
    """
    View a specific version of a document.
    """
    document = get_object_or_404(Document, pk=pk)
    version = get_object_or_404(DocumentVersion, document=document, version_number=version_number)
    
    # Check permission
    if not has_document_permission(request.user, document):
        raise Http404("You don't have permission to view this document.")
    
    return render(request, 'documents/document_version_detail.html', {
        'document': document,
        'version': version
    })


@login_required
def document_version_restore(request, pk, version_number):
    """
    Restore a document to a specific version.
    """
    document = get_object_or_404(Document, pk=pk)
    version = get_object_or_404(DocumentVersion, document=document, version_number=version_number)
    
    # Check permission
    if not (request.user.is_super_admin() or 
            (request.user.is_department_admin() and 
             request.user.department == document.department)):
        messages.error(request, "You don't have permission to restore this document.")
        return redirect('document_detail', pk=pk)
    
    # Create new version with current file
    new_version_number = document.version + 1
    DocumentVersion.objects.create(
        document=document,
        version_number=new_version_number,
        file=document.file,
        uploaded_by=request.user,
        change_notes="Current version before restore"
    )
    
    # Restore the selected version
    document.file = version.file
    document.version = new_version_number
    document.save()
    
    messages.success(request, f'Document restored to version {version_number}. New version created: {new_version_number}')
    log_activity(
        user=request.user,
        action='version_restore',
        object_type='Document',
        object_id=document.id,
        request=request
    )
    
    return redirect('document_detail', pk=pk)
