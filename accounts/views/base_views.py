from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

from accounts.forms.sign_in_form import LoginForm


class SignInView(LoginView):
    view_name = 'login'
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class HomeView(LoginRequiredMixin, TemplateView):
    view_name = 'home'
    template_name = 'accounts/home.html'
    login_url = reverse_lazy(SignInView.view_name)
