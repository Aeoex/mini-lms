from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

app_name = "api-v1"

urlpatterns = [
    # registration
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration",
    ),
    # jwt
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("jwt/logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
    # password
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    # profile
    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
]