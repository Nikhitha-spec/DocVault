from django.urls import path
from .views import (
    PermissionListView,
    PermissionCreateView,
    PermissionDeleteView,
    assign_permission,
)

app_name = 'permissions_app'

urlpatterns = [
    path('', PermissionListView.as_view(), name='permission_list'),
    path('create/', PermissionCreateView.as_view(), name='permission_create'),
    path('<int:pk>/delete/', PermissionDeleteView.as_view(), name='permission_delete'),
    path('assign/<int:document_id>/', assign_permission, name='assign_permission'),
]
