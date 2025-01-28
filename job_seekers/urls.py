from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import UserDetailView, LoginAPIView, LogoutAPIView

router = DefaultRouter()
router.register('profiles', JobSeekerProfileViewSet, basename='jobseeker-profile')

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),  
    path('auth/registration/', JobSeekerRegistrationView.as_view(), name='jobseeker-register'),  
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('dashboard/', JobSeekerDashboardView.as_view(), name='jobseeker-dashboard'),
    path('', include(router.urls)),
    path('applications/', JobSeekerApplicationsView.as_view(), name='jobseeker-applications'),
    path('profile/', JobSeekerProfileDetailView.as_view(), name='jobseeker-profile-detail'),
    path('profile/edit/', JobSeekerProfileUpdateView.as_view(), name='jobseeker-profile-update'),
]
