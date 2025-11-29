from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView

from accounts.create_user_service import UserCreateService
from accounts.forms.sign_in_form import LoginForm
from accounts.forms.create_user_form import CreateUserForm
from accounts.mixins import CanCreateUserMixin


class SignInView(LoginView):
    view_name = 'login'
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class HomeView(LoginRequiredMixin, TemplateView):
    view_name = 'home'
    template_name = 'accounts/home.html'
    login_url = reverse_lazy(SignInView.view_name)


class CreateUserView(LoginRequiredMixin, CanCreateUserMixin, FormView):
    view_name = 'create_user'

    template_name = 'accounts/create_user.html'
    form_class = CreateUserForm
    success_url = reverse_lazy(HomeView.view_name)
    login_url = reverse_lazy(SignInView.view_name)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            user = UserCreateService.create_user(
                username=data['username'],
                password=data['password1'],
                email=data.get('email', ''),
                created_by=self.request.user,
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                group_name=data['user_group'],
                license_count = data.get('license_count')
            )
            messages.success(self.request, f"Account created for {user.username} in group {data['user_group']}!")
        except PermissionError as e:
            form.add_error('user_group', str(e))
            return self.form_invalid(form)
        return super().form_valid(form)
