from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts.models import User

from .emails import sendRegistrationMessage
from core.tokens import account_verification_token
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "phone_number",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "is_active", "role", "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, trim_whitespace=True)
    last_name = serializers.CharField(max_length=50, trim_whitespace=True)
    email = serializers.EmailField()
    phone_number = PhoneNumberField(
        region="NG",
        required=True,
        error_messages={
            "invalid": "Please enter a valid Nigerian phone number",
            "required": "Phone number is required",
        },
    )
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        with transaction.atomic():
            user = User.objects.create_user(**validated_data, is_active=False)
            verification_token = account_verification_token.make_token(user=user)

            transaction.on_commit(
                lambda: sendRegistrationMessage(
                    user=user, token=verification_token
                )
            )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        token = attrs['token']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Invalid verification credentials.'})

        if user.is_active:
            raise serializers.ValidationError({'email': 'Email is already verified.'})

        if not account_verification_token.check_token(user=user, token=token):
            raise serializers.ValidationError({"token": "Invalid or expired verification token"})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save(update_fields=['is_active'])
        return user

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email does not exist.")
        return value

    def validate(self, attrs):
        email = attrs['email']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Invalid verification credentials.'})

        if user.is_active:
            raise serializers.ValidationError({'email': 'Email is already verified.'})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        verification_token = account_verification_token.make_token(user=user)

        sendRegistrationMessage(user=user, token=verification_token)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email does not exist.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email__iexact=email)
        # Generate and send password reset token
        return user

