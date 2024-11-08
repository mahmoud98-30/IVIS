from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.serializers import LoginSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(APIView):
    """
    API view for user registration
    """

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User registered successfully!",
                examples={"application/json": {"message": "User registered successfully!"}}
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                examples={"application/json": {"username": ["This field is required."]}}
            ),
        }
    )
    def post(self, request):
        """
        Register a new user

        :param request: Request object
        :return: Response object
        """

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "refresh": "your_refresh_token",
                        "access": "your_access_token",
                        "user_id": 1,
                        "username": "your_username",
                        "cube_data": {
                            "x": [0, 1, 1, 0, 0, 1, 1, 0],
                            "y": [0, 0, 1, 1, 0, 0, 1, 1],
                            "z": [0, 0, 0, 0, 1, 1, 1, 1],
                            "color": "green",
                            "edge_color": "black"
                        }
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                examples={"application/json": {"non_field_errors": ["Unable to log in with provided credentials."]}}
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class LogoutView(APIView):
    """
    API view for logging out
    """
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            },
            required=['refresh']
        ),
        responses={
            status.HTTP_205_RESET_CONTENT: openapi.Response(
                description="Logout successful",
                examples={"application/json": {"message": "Logout successful!"}}
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                examples={"application/json": {"error": "Invalid token"}}
            ),
        }
    )
    def post(self, request):
        """
        Logout

        :param request: Request object
        :return: Response object
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
