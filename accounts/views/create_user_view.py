from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms.create_user_form import CreateUserForm
from accounts.mixins import AdminAccessMixin
from accounts.services import UserCreateService


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