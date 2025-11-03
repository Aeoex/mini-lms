from django.urls import path, include


app_name = "quiz"

urlpatterns = [
    path("api/v1/", include("quiz.api.v1.urls")),
]