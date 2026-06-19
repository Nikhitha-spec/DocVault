from .models import ActivityLog


def log_activity(user, action, object_type, object_id=None, description='', request=None):
    """
    Log an activity to the database.
    
    Args:
        user: The user who performed the action
        action: The action performed (e.g., 'login', 'upload', 'download')
        object_type: The type of object affected (e.g., 'Document', 'User')
        object_id: The ID of the object affected (optional)
        description: Additional description (optional)
        request: The HTTP request object (optional, used to get IP address)
    """
    ip_address = None
    if request:
        # Get IP address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=object_id,
        description=description,
        ip_address=ip_address
    )


def get_recent_activities(user, limit=10):
    """
    Get recent activities for a user.
    
    Args:
        user: The user object
        limit: Maximum number of activities to return
    
    Returns:
        QuerySet: Recent activities
    """
    queryset = ActivityLog.objects.filter(user=user)
    
    # Department admins see department activities
    if user.is_department_admin():
        from accounts.models import User
        dept_users = User.objects.filter(department=user.department)
        queryset = ActivityLog.objects.filter(user__in=dept_users)
    
    return queryset.order_by('-timestamp')[:limit]
