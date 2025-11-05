from django.db import models
from django.core.validators import MaxValueValidator

from quiz.models import QuizAttempt

# Create your models here.
class Enrollment(models.Model):
    user_profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name='enrollments')
    user_role = models.CharField(max_length=10, blank=True, null=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name='enrollments')
    current_lesson = models.IntegerField(null=True, blank=True)
    final_grade = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    def save(self, *args, **kwargs):
        if not self.user_role and self.user_profile:
            self.user_role = self.user_profile.user.role
        super().save(*args, **kwargs)

    def is_user_enrolled(self, user):
        if not user or not hasattr(user, "profile"):
            return False
        print(self.user_profile == user.profile)
        return self.user_profile == user.profile
    
    def calculate_final_grade(self):
        average_score = QuizAttempt.objects.filter(
                            quiz__lesson__course=self.course
                        ).aggregate(models.Avg("score"))["score__avg"]
        return average_score
