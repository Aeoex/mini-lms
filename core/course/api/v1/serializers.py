from django.utils import timezone
from rest_framework import serializers
from ...models import Lesson, Course



class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True,
    )
    relative_url = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "relative_url", "absolute_url"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_api_url())

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["course"] = instance.course.title
        request = self.context.get("request")
        if request:
            path = request.path.rstrip("/")  # remove trailing slash
            last_segment = path.split("/")[-1]

            # if the last part of the URL is a number, it's a detail endpoint like /lessons/5/
            if last_segment.isdigit():
                rep.pop("relative_url", None)
                rep.pop("absolute_url", None)
        return rep
    
class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SlugRelatedField(
        many=True,
        slug_field="title",
        read_only=True
    )
    relative_url = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Course
        fields = ["id", "title", "description", "start_date", "end_date", "lessons", "relative_url", "absolute_url"]
    
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_api_url())
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        return rep
