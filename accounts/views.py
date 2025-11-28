from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView

from accounts.forms import LoginForm, CreateUserForm


class SignInView(LoginView):
    view_name = 'login'
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class HomeView(LoginRequiredMixin, TemplateView):
    view_name = 'home'
    template_name = 'accounts/home.html'
    login_url = reverse_lazy(SignInView.view_name)


class CreateUserView(LoginRequiredMixin, CreateView):
    view_name = 'create_user'
    template_name = 'accounts/create_user.html'
    form_class = CreateUserForm
    success_url = reverse_lazy(HomeView.view_name)
    login_url = reverse_lazy(SignInView.view_name)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        group_name = user.groups.first().name if user.groups.exists() else "No Group"

        messages.success(self.request, f"Account created for {user.username} in group {group_name}!")
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)