from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'complaints', views.ComplaintViewSet)
router.register(r'departments', views.DepartmentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls
