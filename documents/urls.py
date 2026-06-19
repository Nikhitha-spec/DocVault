from django.urls import path
from .views import (
    DocumentListView,
    DocumentDetailView,
    DocumentCreateView,
    DocumentUpdateView,
    DocumentDeleteView,
    document_download,
    document_preview,
    document_replace,
    document_restore,
    document_version_detail,
    document_version_restore,
)

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('create/', DocumentCreateView.as_view(), name='document_create'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('<int:pk>/update/', DocumentUpdateView.as_view(), name='document_update'),
    path('<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
    path('<int:pk>/download/', document_download, name='document_download'),
    path('<int:pk>/preview/', document_preview, name='document_preview'),
    path('<int:pk>/replace/', document_replace, name='document_replace'),
    path('<int:pk>/restore/', document_restore, name='document_restore'),
    path('<int:pk>/version/<int:version_number>/', document_version_detail, name='document_version_detail'),
    path('<int:pk>/version/<int:version_number>/restore/', document_version_restore, name='document_version_restore'),
]
