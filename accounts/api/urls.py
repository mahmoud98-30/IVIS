"""
Authentication and Profile API endpoints
========================================

This module contains the API endpoints for user authentication and
profile management.

Endpoints:

- `register/`: Register a new user
- `verify-otp/`: Verify OTP for a user
- `login/`: Login a user
- `logout/`: Logout a user
- `token/refresh/`: Refresh token for a user
- `token/verify/`: Verify token for a user
- `change-password/`: Change password for a user
- `profile/detail/`: Get user profile
- `profile/edit/`: Edit user profile
- `user-types-list/`: Get user types

"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationAPIView, LoginView, LogoutView

urlpatterns = [
    # AUTHENTICATION API
    path('register/', UserRegistrationAPIView.as_view(), name='register'),  # Register User
    path('login/', LoginView.as_view(), name='login'),  # Login User
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'), # Refresh Token

    path('logout/', LogoutView.as_view(), name='logout'),  # Logout User


]


