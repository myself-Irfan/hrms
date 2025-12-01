from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView

from accounts.enums import UserGroup
from accounts.services import UserCreateService, UserListService
from accounts.forms.sign_in_form import LoginForm
from accounts.forms.create_user_form import CreateUserForm
from accounts.mixins import AdminAccessMixin



class SignInView(LoginView):
    view_name = 'login'
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class HomeView(LoginRequiredMixin, TemplateView):
    view_name = 'home'
    template_name = 'accounts/home.html'
    login_url = reverse_lazy(SignInView.view_name)


class CreateUserView(LoginRequiredMixin, AdminAccessMixin, FormView):
    view_name = 'create_user'
    permission_denied_message = "You don't have permission to create users."

    template_name = 'accounts/create_user.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

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
                license_count=data.get('license_count')
            )
            messages.success(self.request, f"Account created for {user.username}!")
        except PermissionError as e:
            form.add_error('user_group', str(e))
            return self.form_invalid(form)
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, AdminAccessMixin, ListView):
    view_name = 'list_users'
    permission_denied_message = "You don't have permission to view the user list."

    template_name = 'accounts/list_users.html'
    context_object_name = 'users'
    paginate_by = 20
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return UserListService.get_users_for_list(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = UserListService.get_user_statistics(self.request.user)
        context['total_users'] = stats['total']
        context['reseller_admins_count'] = stats['reseller_admins']
        context['client_admins_count'] = stats['client_admins']

        # Add current user's role
        if self.request.user.is_superuser:
            context['current_user_role'] = UserGroup.SUPER_ADMIN
        else:
            user_group = self.request.user.groups.first()
            context['current_user_role'] = user_group.label if user_group else 'Unknown'

        return context