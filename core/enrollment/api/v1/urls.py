from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"


router = DefaultRouter()

router.register(r"enrollments", views.EnrollmentModelViewSet, basename="enrollments")

urlpatterns = router.urls