from django.db import models
from django.core.exceptions import ValidationError
from .tasks import course_ended
from django.utils.timezone import make_aware
from datetime import datetime

from enrollment.models import Enrollment


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    instructor = models.ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True, related_name="courses")

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
        
    def __str__(self):
        return f"{self.title}"
    
    def is_user_enrolled(self, user):
        return Enrollment.objects.filter(user_profile=user.profile, course=self).exists()
    
    def get_absolute_api_url(self):
        return f"/course/api/v1/courses/{self.pk}/"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_end_date = None

        if not is_new:
            old_end_date = Course.objects.get(pk=self.pk).end_date

        super().save(*args, **kwargs)

        if is_new or self.end_date != old_end_date:
            run_at = make_aware(datetime.combine(self.end_date, datetime.min.time()))
            course_ended.apply_async((self.id,), eta=run_at)


class Lesson(models.Model):
    title = models.CharField(max_length=500)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="lessons")
    quiz = models.OneToOneField("quiz.Quiz", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_api_url(self):
        return f"/course/api/v1/lessons/{self.pk}/"
    
    def is_user_enrolled(self, user):
        return Enrollment.objects.filter(user_profile=user.profile, course=self.course).exists()

