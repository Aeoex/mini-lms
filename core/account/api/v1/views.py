from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ...models import CustomUser, Profile
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    CustomChangePasswordSerializer,
    ProfileSerializer,
    
)

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serialized = RegistrationSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            email = serialized.validated_data["email"]
            data = {"email": email}

            # from some other code, i probably wont use this for
            # this mini lms project

            # user = get_object_or_404(CustomUser, email=email)
            # refresh = RefreshToken.for_user(user)
            # token = str(refresh.access_token)
            # message = EmailMessage(
            #     "email/activation.tpl",
            #     {"token": token},
            #     "ad@ad.com",
            #     to=[email],
            # )
            # EmailThread(message).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = CustomChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serialized = self.get_serializer(data=request.data)

        if serialized.is_valid():
            if not self.object.check_password(
                serialized.validated_data.get("old_password")
            ):
                return Response(
                    {"old_password": "Wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(
                serialized.validated_data.get("new_password")
            )
            self.object.save()
            return Response(
                {"detail": "password set"}, status=status.HTTP_200_OK
            )
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user=self.request.user)

    http_method_names = ['get', 'put', 'head', 'options']