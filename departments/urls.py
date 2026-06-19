from django.urls import path
from .views import (
    DepartmentListView,
    DepartmentCreateView,
    DepartmentUpdateView,
    DepartmentDeleteView,
)

app_name = 'departments'

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department_list'),
    path('create/', DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/update/', DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
]
