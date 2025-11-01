from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    manager for the custom user
    """

    def create_student(self, email, password, **extra_fields):
        """
        create a new student
        """
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_instructor(self, email, password, **extra_fields):
        """
        create new instructor
        """
        extra_fields.setdefault("role", 'instructor')
        if extra_fields.get("role") is not 'instructor':
            raise ValueError(_("instructor user must have role=instructor"))
        if not email:
            raise ValueError(_("The email must be set"))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    custom user model for this lms app
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
