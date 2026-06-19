from django.urls import path
from .views import (
    RoleListView,
    RoleCreateView,
    RoleUpdateView,
    RoleDeleteView,
)

app_name = 'roles'

urlpatterns = [
    path('', RoleListView.as_view(), name='role_list'),
    path('create/', RoleCreateView.as_view(), name='role_create'),
    path('<int:pk>/update/', RoleUpdateView.as_view(), name='role_update'),
    path('<int:pk>/delete/', RoleDeleteView.as_view(), name='role_delete'),
]
