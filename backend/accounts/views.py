from django.conf import settings
from django.db import transaction
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


# from rest_framework.response import Response
from accounts.models import User

from .emails import sendRegistrationMessage
from .serializers import CreateUserSerializer, UserSerializer, VerifyEmailSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        sendRegistrationMessage(user=user)

        return Response(
            {
                "message": (
                    f"Welcome to {settings.PROJECT_NAME}! Please check your email to confirm your account."
                )
            },
            status=status.HTTP_201_CREATED,
        )


