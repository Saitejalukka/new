
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    ProfileSerializer
)


@api_view(['GET'])
def user_api_root(request, format=None):
    """
    An API root view that lists all authentication and user endpoints available.
    """
    return Response({
        'register': reverse('users:register', request=request, format=format),
        'profile': reverse('users:profile', request=request, format=format),
        'logout': reverse('users:logout', request=request, format=format),
    })


class RegisterView(generics.CreateAPIView):
    """
    Handles new user registration.
    Allows unauthenticated (AllowAny) access.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Handles retrieving and updating the authenticated user's profile.
    Requires authentication (IsAuthenticated).
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    Handles user logout by blacklisting the provided JWT refresh token.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {'message': 'Successfully logged out.'},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {'error': 'Invalid or expired refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )