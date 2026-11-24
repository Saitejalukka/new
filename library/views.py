from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


# Create your views here.


User = get_user_model()


# 1. User Registration API
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [permissions.AllowAny]


# 2. User Login API
class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        from django.contrib.auth import authenticate

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# 3. User Profile API
class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        })
