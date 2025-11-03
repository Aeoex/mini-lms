from django.urls import path, include


app_name = "enrollment"

urlpatterns = [
    path("api/v1/", include("enrollment.api.v1.urls")),
]