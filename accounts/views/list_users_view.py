from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from accounts.enums import UserGroup
from accounts.mixins import AdminAccessMixin
from accounts.services import UserListService


class ListUserView(LoginRequiredMixin, AdminAccessMixin, ListView):
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

        if self.request.user.is_superuser:
            context['current_user_role'] = UserGroup.SUPER_ADMIN
        else:
            user_group = self.request.user.groups.first()
            context['current_user_role'] = user_group.label if user_group else 'Unknown'

        return context