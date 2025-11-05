from celery import shared_task


from enrollment.models import Enrollment

@shared_task
def course_ended(course_id):
    from .models import Course
    course = Course.objects.get(id=course_id)
    enrollments = list(Enrollment.objects.filter(course=course))
    # for e in enrollments:
    #     e.final_grade = e.calculate_final_grade()
    # Enrollment.objects.bulk_update(enrollments, ['final_grade'])
    print(f"Course {course.title} has ended!")
