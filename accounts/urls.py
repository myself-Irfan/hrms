from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views.base_views import SignInView, HomeView
from accounts.views.create_user_view import CreateUserView
from accounts.views.edit_user_view import EditUserView
from accounts.views.list_users_view import ListUserView


urlpatterns = [
    path('login/', SignInView.as_view(), name=SignInView.view_name),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name=HomeView.view_name),
    path('create_user/', CreateUserView.as_view(), name=CreateUserView.view_name),
    path('list_users/', ListUserView.as_view(), name=ListUserView.view_name),
    path('edit_user/<int:pk>',EditUserView.as_view(), name=EditUserView.view_name)
]