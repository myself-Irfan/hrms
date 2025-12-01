from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.models import ClientLicenseInfo
from accounts.services.user_update_service import UserUpdateService
from accounts.forms.edit_user_form import EditUserForm
from accounts.mixins import AdminAccessMixin


class EditUserView(LoginRequiredMixin, AdminAccessMixin, FormView):
    view_name = 'edit_user'
    permission_denied_message = "You don't have permission to edit users."

    template_name = 'accounts/edit_user.html'
    form_class = EditUserForm
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, pk=kwargs.get('pk'))

        can_edit, error_msg = UserUpdateService.can_edit_user(request.user, self.user_instance)
        if not can_edit:
            messages.error(request, error_msg)
            return redirect('user_list')

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.user_instance
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_instance'] = self.user_instance

        user_group = self.user_instance.groups.first()
        context['user_role'] = user_group.name if user_group else 'No Group'

        # Get license info
        try:
            context['license_info'] = self.user_instance.license_info
        except ClientLicenseInfo.DoesNotExist:
            context['license_info'] = None

        return context

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            UserUpdateService.update_user(
                user=self.user_instance,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=data.get('password') if data.get('password') else None,
                license_count=data.get('license_count'),
                is_active=data.get('is_active', True)
            )
            messages.success(
                self.request,
                f"User '{self.user_instance.username}' has been updated successfully!"
            )
            return redirect('user_list')
        except ValueError as e:
            form.add_error('license_count', str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Error updating user: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('user_list')