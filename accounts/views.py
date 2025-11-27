from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserCreateSerializer


class LoginView(TokenObtainPairView):
    api_name = 'login'

    permission_classes = (permissions.AllowAny, )


class CreateUserView(generics.CreateAPIView):
    api_name = 'register_user'

    serializer_class = UserCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)