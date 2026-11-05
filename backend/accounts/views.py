from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
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

        email = serializer.validated_data['email']
        phone_number = serializer.validated_data['phone_number']

        try:
            user = serializer.save()
        except IntegrityError:
            if User.objects.filter(email__iexact=email).exists():
                return Response(
                    {"message": "A user with this email already exists."},
                    status=status.HTTP_409_CONFLICT,
                )

            if User.objects.filter(phone_number=phone_number).exists():
                return Response({
                    "message": "A user with this phone number already exists."
                }, status=status.HTTP_409_CONFLICT)

            raise

        return Response(
            {
                "message": (
                    f"Welcome to {settings.PROJECT_NAME}! Please check your email to confirm your account."
                )
            },
            status=status.HTTP_201_CREATED,
        )


