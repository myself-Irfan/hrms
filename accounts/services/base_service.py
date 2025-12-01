from django.contrib.auth.models import User

from accounts.enums import UserGroup


class BaseUserService:
    @staticmethod
    def can_access_admin_features(user: User) -> bool:
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        user_group = user.groups.first()
        if not user_group:
            return False

        allowed_roles = [UserGroup.SUPER_ADMIN, UserGroup.RESELLER_ADMIN]
        return user_group.name in allowed_roles

    @staticmethod
    def get_user_role(user: User) -> UserGroup | None:
        if not user or not user.is_authenticated:
            return None

        if user.is_superuser:
            return UserGroup.SUPER_ADMIN

        user_group = user.groups.first()
        if not user_group:
            return None

        try:
            return UserGroup(user_group.name)
        except ValueError:
            return None

    @staticmethod
    def is_super_admin_or_above(user: User) -> bool:
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        user_group = user.groups.first()
        return user_group and user_group.name == UserGroup.SUPER_ADMIN

    @staticmethod
    def is_reseller_admin(user: User) -> bool:
        if not user or not user.is_authenticated:
            return False

        user_group = user.groups.first()
        return user_group and user_group.name == UserGroup.RESELLER_ADMIN