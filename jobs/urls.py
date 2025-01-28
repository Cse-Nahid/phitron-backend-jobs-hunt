from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job')
router.register('categories', JobCategoryViewSet, basename='job-category')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', JobSearchView.as_view(), name='job-search'),
    path('jobs/create/', JobCreateView.as_view(), name='create-job'),
    path('jobs/<int:pk>', JobDetailView.as_view(), name='job-detail'),
    path('categories/', JobCategoryViewSet.as_view({'get': 'list'}), name='job-category-list'),
    path('categories/<int:pk>/', JobCategoryDetailView.as_view(), name='job-category-detail'), 
]

