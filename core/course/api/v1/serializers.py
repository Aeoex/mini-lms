from django.utils import timezone
from rest_framework import serializers
from ...models import Lesson, Course



class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True,
    )
    class Meta:
        model = Lesson
        fields = ["id", "title", "course"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["course"] = instance.course.title
        return rep
    
class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SlugRelatedField(
        many=True,
        slug_field="title",
        read_only=True
    )
    class Meta:
        model = Course
        fields = ["id", "title", "description", "start_date", "end_date", "lessons"]
