from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Quiz(models.Model):
    result = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

class Question(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()

class Choice(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="choices")
    content = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)