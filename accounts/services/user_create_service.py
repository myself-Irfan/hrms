from django.contrib.auth.models import User, Group
from django.db import transaction

from accounts.enums import UserGroup
from accounts.models import ClientLicenseInfo
from accounts.services.base_service import BaseUserService


class UserCreateService(BaseUserService):
    @staticmethod
    def ensure_groups_exist():
        for group_value, _ in UserGroup.choices:
            Group.objects.get_or_create(name=group_value)

    @staticmethod
    def get_allowed_groups(current_user: User):
        if not current_user:
            return []

        if current_user.is_superuser:
            return [UserGroup.SUPER_ADMIN, UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN]

        group = current_user.groups.first()
        if not group:
            return []

        role_permissions = {
            UserGroup.SUPER_ADMIN: [UserGroup.SUPER_ADMIN, UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN],
            UserGroup.RESELLER_ADMIN: [UserGroup.CLIENT_ADMIN]
        }
        return role_permissions.get(group.name, [])

    @staticmethod
    def check_license_availability(creator: User, target_group: str):
        if creator.is_superuser:
            return True, None

        creator_group = creator.groups.first()
        if not creator_group:
            return False, "Creator has no group assigned."

        if creator_group.name not in [UserGroup.RESELLER_ADMIN, UserGroup.CLIENT_ADMIN]:
            return True, None

        try:
            license_info = creator.license_info
        except ClientLicenseInfo.DoesNotExist:
            return False, "No license information found for your account."

        if not license_info.can_create_user():
            return False, f"License limit reached. You have used {license_info.used_licenses}/{license_info.total_licenses} licenses."

        return True, None

    @staticmethod
    @transaction.atomic
    def create_user(username, password, email, group_name, created_by, first_name='', last_name='', license_count=None):
        can_create, error_msg = UserCreateService.check_license_availability(created_by, group_name)
        if not can_create:
            raise PermissionError(error_msg)

        # Create the user
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.clear()
        user.groups.add(group)

        if group_name in [UserGroup.CLIENT_ADMIN, UserGroup.RESELLER_ADMIN] and license_count:
            ClientLicenseInfo.objects.create(
                user=user,
                total_licenses=license_count,
                used_licenses=0,
                created_by=created_by
            )

        if not created_by.is_superuser:
            try:
                creator_license = created_by.license_info
                creator_license.used_licenses += 1
                creator_license.save()
            except ClientLicenseInfo.DoesNotExist:
                pass

        return user

    @staticmethod
    def validate_user_data(current_user: User, group_name: str):
        allowed_groups = UserCreateService.get_allowed_groups(current_user)
        if group_name not in allowed_groups:
            raise PermissionError(f"You don't have permission to assign {group_name}.")