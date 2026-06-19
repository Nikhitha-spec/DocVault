from django.urls import path
from .views import ActivityLogListView
from django.utils.decorators import method_decorator

app_name = 'activity_logs'

urlpatterns = [
    path('', ActivityLogListView.as_view(), name='activity_log_list'),
]
