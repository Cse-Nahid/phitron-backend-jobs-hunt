# contact_us/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.ContactusViewset)

urlpatterns = router.urls  # Just use the router's URLs, no need for extra path definitions
