from rest_framework import serializers
from accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
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
        confirm_password = validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user
