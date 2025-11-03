from django.urls import path, include


app_name = "course"

urlpatterns = [
    path("api/v1/", include("course.api.v1.urls")),
]