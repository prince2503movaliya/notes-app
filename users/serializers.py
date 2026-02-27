from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from utils.response import error_response


class CustomTokenSerializer(TokenObtainPairSerializer):


     @classmethod
     def get_token(cls, user):
            token = super().get_token(user)

            # 🔥 Add custom data in JWT
            token['email'] = user.email
            token['name'] = user.name

            return token
        

     def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # 🔹 Validate input
        if not email or not password:
            raise serializers.ValidationError(
                error_response(message="Email and password are required")
            )

        # 🔹 Authenticate user (IMPORTANT FIX)
        user = authenticate(
            username=email,   # ✅ correct way
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                error_response(message="Invalid credentials")
            )

        # 🔐 Security checks
        if not user.is_active:
            raise serializers.ValidationError(
                error_response(message="User account is disabled")
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                error_response(message="Account not verified")
            )

        # 🔹 Generate token
        data = super().validate({
            "username": user.email,
            "password": password
        })

        # 🔹 Add extra response data
        data.update({
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        })

        return data