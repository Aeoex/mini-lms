from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"


router = DefaultRouter()

router.register(r"quizzes", views.QuizModelViewSet, basename="quizzes")
router.register(r'questions', views.QuestionViewSet, basename="questions")
router.register(r'choices', views.ChoiceViewSet, basename="choices")

urlpatterns = router.urls + [
    path("quiz-attempts/<int:pk>/", views.QuizAttemptRetrieveAPIView.as_view(), name="quiz-attempt-retrieve"),
    path("quiz-attempts/", views.QuizAttemptListAPIView.as_view(), name="quiz-attempts"),
]