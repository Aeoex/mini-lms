from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Enrollment(models.Model):
    user_profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name='profiles')
    user_role = models.CharField(max_length=10)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name='courses')
    current_lesson = models.IntegerField(null=True, blank=True)
    final_grade = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])