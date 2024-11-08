from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation, authenticate


# The UserRegistrationSerializer is used to register a new user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not needed in user creation
        user = User.objects.create_user(**validated_data)
        return user





from rest_framework import serializers, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        # This calls the parent's validate method, which checks the username and password
        data = super().validate(attrs)

        # Simulate "cube" data points
        cube_data = {
            'x': [0, 1, 1, 0, 0, 1, 1, 0],  # x-coordinates for a cube's vertices
            'y': [0, 0, 1, 1, 0, 0, 1, 1],  # y-coordinates for a cube's vertices
            'z': [0, 0, 0, 0, 1, 1, 1, 1],  # z-coordinates for a cube's vertices
            'color': 'green',
            'edge_color': 'black'
        }

        # Add user-specific information to the response data
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'cube_data': cube_data  # Include cube data
        })
        return data


