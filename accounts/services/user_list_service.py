from django.contrib.auth.models import User

from accounts.enums import UserGroup
from accounts.services.base_service import BaseUserService


class UserListService(BaseUserService):
    @staticmethod
    def get_users_for_list(current_user: User):
        if not current_user or not current_user.is_authenticated:
            return User.objects.none()

        if UserListService.is_super_admin_or_above(current_user):
            return User.objects.filter(
                groups__name__in=[UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN]
            ).select_related('license_info').prefetch_related('groups').distinct().order_by('-date_joined')

        if UserListService.is_reseller_admin(current_user):
            return User.objects.filter(
                groups__name=UserGroup.CLIENT_ADMIN,
                license_info__created_by=current_user
            ).select_related('license_info').prefetch_related('groups').distinct().order_by('-date_joined')

        # Others see nothing
        return User.objects.none()

    @staticmethod
    def get_user_statistics(current_user: User):
        """Get statistics about users visible to current_user"""
        users = UserListService.get_users_for_list(current_user)

        total_users = users.count()
        reseller_admins = users.filter(groups__name=UserGroup.RESELLER_ADMIN).count()
        client_admins = users.filter(groups__name=UserGroup.CLIENT_ADMIN).count()

        return {
            'total': total_users,
            'reseller_admins': reseller_admins,
            'client_admins': client_admins,
        }