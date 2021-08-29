from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from app_tests.models import Result
from app_tests.serializers import ResultSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = super().create(validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "results",
        ]

    def get_results(self, obj):
        return ResultSerializer(
            Result.objects.filter(user=obj), many=True
        ).data
