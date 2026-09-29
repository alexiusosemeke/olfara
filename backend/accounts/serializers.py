from rest_framework import serializers
from accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
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


class RegisterUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        region="NG",
        required=True,
        error_messages={
            "invalid": "Please enter a valid Nigerian phone number",
            "required": "Phone number is required",
        },
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "password",
            "role",
            "phone_number",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "is_active", "role", "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

        def validate(self, attrs):

            validate_password(attrs["password"])
            email = attrs["email"]
            username = attrs["username"]

            if not username.strip():
                raise serializers.ValidationError(
                    {"username": "Username cannot be empty"}
                )

            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "A user with this email already exists"}
                )

            return attrs

        def create(self, validated_data):

            password = validated_data.pop("password")

            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()

            return user
