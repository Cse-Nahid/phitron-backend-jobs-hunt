from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import UserDetailView, LoginAPIView, LogoutAPIView

router = DefaultRouter()
router.register('profiles', EmployerProfileViewSet, basename='employer-profile')

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', EmployerRegistrationView.as_view(), name='employer-register'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('dashboard/', EmployerDashboardView.as_view(), name='employer-dashboard'),
    path('', include(router.urls)),
    path('applications/', EmployerApplicationsView.as_view(), name='employer-applications'),
    path('profile/', EmployerProfileDetailView.as_view(), name='employer-profile-detail'),
    path('profile/edit/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
]
