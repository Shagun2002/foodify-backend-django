from django.contrib.auth.models import User
from rest_framework import serializers, validators
from .models import CustomUser

# from django.contrib.auth import get_user_model
# User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")

        # defining email and password properties
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        CustomUser.objects.all(), "A user with email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        email= validated_data.get("email")
        password = validated_data.get("password")

        user = CustomUser.objects.create_user(email=email, password=password)
        return user
