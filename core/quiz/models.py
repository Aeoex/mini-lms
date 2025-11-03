from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Quiz(models.Model):
    def __str__(self):
        return f"quiz for {self.lesson.title}" if hasattr(self, "lesson") and self.lesson else f"Quiz {self.id}"


class Question(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()

class Choice(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="choices")
    content = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

class QuizAttempt(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="attempts")
    enrollment = models.ForeignKey("enrollment.Enrollment", on_delete=models.CASCADE, related_name="quiz_attempts")
    score = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("quiz", "enrollment")

    def __str__(self):
        return f"{self.enrollment.user_profile.user.email} - {self.quiz.lesson.title} ({self.score}%)"
