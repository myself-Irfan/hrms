from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.services import BaseUserService


class AdminAccessMixin(UserPassesTestMixin):
    permission_denied_message = "You don't have permission to access this page."

    def test_func(self):
        return BaseUserService.can_access_admin_features(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy('home'))