from django.contrib.auth.models import User, Group
from accounts.enums import UserGroup
from accounts.models import ClientLicenseInfo


class UserCreateService:
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
            UserGroup.RESELLER_ADMIN: [UserGroup.CLIENT_ADMIN],
            UserGroup.CLIENT_ADMIN: [UserGroup.BASE_USER],
            UserGroup.BASE_USER: [],
        }
        return role_permissions.get(group.name, [])

    @staticmethod
    def create_user(username, password, email, group_name, created_by, first_name='', last_name='', license_count=None):
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.clear()
        user.groups.add(group)

        if group_name in [UserGroup.CLIENT_ADMIN.value, UserGroup.RESELLER_ADMIN.value] and license_count:
            ClientLicenseInfo.objects.create(
                user=user,
                license_count=license_count,
                created_by=created_by
            )

        return user

    @staticmethod
    def validate_user_data(current_user: User, group_name: str):
        allowed_groups = UserCreateService.get_allowed_groups(current_user)
        if group_name not in allowed_groups:
            raise PermissionError(f"You don't have permission to assign {group_name}.")
