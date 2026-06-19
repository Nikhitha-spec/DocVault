from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LoginAPIView,
    LogoutAPIView,
    UserViewSet,
    DepartmentViewSet,
    DocumentViewSet,
    PermissionViewSet,
    ActivityLogViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'activity-logs', ActivityLogViewSet)

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
