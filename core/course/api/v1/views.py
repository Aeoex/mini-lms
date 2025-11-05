from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ...models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer
from core.permissions import IsInstructorOrAdmin, IsEnrolledInCourse

class LessonModelViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filterset_fields = ['title', 'course__title']
    search_fields = ['title', 'course__title']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Lesson.objects.all()
            return Lesson.objects.filter(course__enrollments__user_profile=user.profile).distinct()
        return Lesson.objects.none()
    
    def get_permissions(self):
        """
        Assign permissions dynamically depending on the action or request method.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsEnrolledInCourse]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsInstructorOrAdmin]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class CourseModelViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ['title', 'instructor__last_name']
    search_fields = ['title', 'instructor__last_name', 'description']

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Assign permissions dynamically depending on the action or request method.
        """
        if self.action in ["list", "retrieve"]:
            # Anyone can view available courses
            permission_classes = [AllowAny]

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            # Only instructors or admins can create/edit/delete courses
            permission_classes = [IsAuthenticated, IsInstructorOrAdmin]

        elif self.action == "lessons":
            # Only enrolled users can view lessons of a course
            permission_classes = [IsAuthenticated, IsEnrolledInCourse]

        else:
            # Default fallback
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]