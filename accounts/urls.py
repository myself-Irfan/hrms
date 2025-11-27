from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import LoginView, CreateUserView


urlpatterns = [
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', LoginView.as_view(), name=LoginView.api_name),
    path('register/', CreateUserView.as_view(), name=CreateUserView.api_name)
]
