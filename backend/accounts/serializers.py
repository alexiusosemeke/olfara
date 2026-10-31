from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts.models import User

from .emails import sendRegistrationMessage
from core.tokens import account_verification_token


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
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
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

    def validate(self, attrs):
        first_name = attrs.get("first_name").strip()
        last_name = attrs.get("last_name").strip()

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if first_name is None:
            raise serializers.ValidationError({"first_name": "First name is required"})

        if last_name is None:
            raise serializers.ValidationError({"last_name": "Last name is required."})

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"A user with this email already exists"})
        return value

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
