from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import SignInView, HomeView, CreateUserView

urlpatterns = [
    path('login/', SignInView.as_view(), name=SignInView.view_name),
    path('', HomeView.as_view(), name=HomeView.view_name),
    path('create_user/', CreateUserView.as_view(), name=CreateUserView.view_name),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]