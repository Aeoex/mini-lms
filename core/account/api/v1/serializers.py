from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

from ...models import CustomUser, Profile
from enrollment.models import Enrollment


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255, write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2", "role"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError(
                {"password": "passwords must match"}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2", None)
        if validated_data.get('role') == 'Instructor' :
            return CustomUser.objects.create_instructor(**validated_data)
        return CustomUser.objects.create_student(**validated_data)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            msg = _("User account is not active.")
            raise serializers.ValidationError(msg, code="inactive account")
        data["email"] = self.user.email
        data["user_id"] = self.user.id
        return data

class CustomChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password2"):
            raise serializers.ValidationError(
                {"new_password": "passwords must match"}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        return super().validate(attrs)
    
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only = True)
    enrollments = serializers.SlugRelatedField(many=True, read_only=True, slug_field="course__title")
    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "image",
            "created_date",
            "updated_date",
            "enrollments"
        ]
        read_only_fields = ["id", "created_date", "updated_date"]