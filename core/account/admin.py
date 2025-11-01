from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_superuser", "is_active", "role")
    list_filter = ("email", "is_superuser", "is_active", "role")
    fieldsets = (
        ("Credentials", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role"
                )
            },
        ),
        (
            "Dates",
            {"fields": ("created_date", "updated_date")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_superuser",
                ),
            },
        ),
    )
    readonly_fields = ("created_date", "updated_date")
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)