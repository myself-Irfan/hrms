from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.enums import UserGroup


class CanCreateUserMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        user_group = user.groups.first()
        if not user_group:
            return False

        allowed_groups = [
            UserGroup.SUPER_ADMIN,
            UserGroup.RESELLER_ADMIN,
            UserGroup.CLIENT_ADMIN
        ]
        return user_group.name in allowed_groups

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You don't have permission to create users."
        )
        return redirect(reverse_lazy('home'))