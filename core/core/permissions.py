from rest_framework.permissions import BasePermission

class IsInstructorOrAdmin(BasePermission):
    """
    Allow only instructors (who own the course) or admins to edit it.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if (
            hasattr(request.user, "profile")
            and request.user.role == "instructor"
        ):
            return True

        return False
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return (
            hasattr(request.user, "profile")
            and request.user.role == "instructor"
            and obj.is_user_enrolled(request.user)
        )


class IsEnrolledInCourse(BasePermission):
    """
    Allow access only to enrolled users (or admins) for a course.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return obj.is_user_enrolled(request.user)