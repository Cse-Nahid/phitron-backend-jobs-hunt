from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationListCreateView, ApplicationDetailView, ApplicationViewSet, ApplicationDeleteView, ApplicationUpdateView

router = DefaultRouter()
router.register('applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('apply/', ApplicationListCreateView.as_view(), name='apply-for-job'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('<int:pk>/edit/', ApplicationUpdateView.as_view(), name='application-edit'),
    path('<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application-delete'),
    path('', include(router.urls)),
]
