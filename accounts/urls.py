from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    dashboard,
    profile,
    ProfileUpdateView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
