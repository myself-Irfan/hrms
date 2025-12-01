from django.contrib.auth.models import User
from django.db import transaction

from accounts.enums import UserGroup
from accounts.models import ClientLicenseInfo
from accounts.services.base_service import BaseUserService


class UserUpdateService(BaseUserService):
    @staticmethod
    def can_edit_user(current_user: User, target_user: User) -> tuple[bool, str | None]:
        if not current_user or not current_user.is_authenticated:
            return False, "You must be logged in."

        if current_user == target_user:
            return False, "You cannot edit your own account through this interface."

        if current_user.is_superuser:
            return True, None

        target_role = BaseUserService.get_user_role(target_user)
        if not target_role:
            return False, "Target user has no group assigned."

        if BaseUserService.is_super_admin_or_above(current_user):
            if target_role in [UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN]:
                return True, None
            return False, "You can only edit Reseller Admins and Client Admins."

        if BaseUserService.is_reseller_admin(current_user):
            if target_role == UserGroup.CLIENT_ADMIN:
                try:
                    if target_user.license_info.created_by == current_user:
                        return True, None
                    return False, "You can only edit Client Admins you created."
                except ClientLicenseInfo.DoesNotExist:
                    return False, "Cannot verify creation relationship."
            return False, "You can only edit Client Admins."

        return False, "You don't have permission to edit users."

    @staticmethod
    def get_editable_users(current_user: User):
        if not current_user or not current_user.is_authenticated:
            return User.objects.none()

        if BaseUserService.is_super_admin_or_above(current_user):
            return User.objects.filter(
                groups__name__in=[UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN]
            ).exclude(id=current_user.id).select_related('license_info').prefetch_related('groups').distinct()

        if BaseUserService.is_reseller_admin(current_user):
            return User.objects.filter(
                groups__name=UserGroup.CLIENT_ADMIN,
                license_info__created_by=current_user
            ).exclude(id=current_user.id).select_related('license_info').prefetch_related('groups').distinct()

        return User.objects.none()

    @staticmethod
    @transaction.atomic
    def update_user(user: User, first_name: str = None, last_name: str = None,
                    email: str = None, password: str = None, license_count: int = None,
                    is_active: bool = None):
        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if email is not None:
            user.email = email

        if password is not None and password:
            user.set_password(password)

        if is_active is not None:
            user.is_active = is_active

        user.save()

        if license_count is not None:
            try:
                license_info = user.license_info
                if license_count >= license_info.used_licenses:
                    license_info.total_licenses = license_count
                    license_info.save()
                else:
                    raise ValueError(
                        f"New license count ({license_count}) cannot be less than "
                        f"used licenses ({license_info.used_licenses})."
                    )
            except ClientLicenseInfo.DoesNotExist:
                pass

        return user