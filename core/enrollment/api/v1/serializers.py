from django.utils import timezone
from rest_framework import serializers
from ...models import Enrollment
from course.models import Course
from account.models import Profile



class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True,
    )
    user_role = serializers.CharField(source="user_profile.user.role", read_only=True)
    class Meta:
        model = Enrollment
        fields = ["id", "course", "user_profile", "user_role", "current_lesson", "final_grade"]
        read_only_fields = ["id", "user_profile", "user_role", "current_lesson", "final_grade"]

    def create(self, validated_data):
        """
        Automatically set user_profile from the current request user.
        """
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            raise serializers.ValidationError("Request user is not available.")

        try:
            validated_data["user_profile"] = request.user.profile
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile not found for current user.")

        if Enrollment.objects.filter(user_profile=validated_data["user_profile"], course=validated_data["course"]).exists():
            raise serializers.ValidationError("User is already enrolled in this course.")
        validated_data["user_role"] = request.user.role
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["course"] = instance.course.title
        rep["user_profile"] = instance.user_profile.user.email
        return rep