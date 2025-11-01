from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
        
    def __str__(self):
        return f"{self.title}"
    
class Lesson(models.Model):
    title = models.CharField(max_length=500)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="lessons")
    quiz = models.OneToOneField("quiz.Quiz", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}"

