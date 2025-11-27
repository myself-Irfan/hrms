from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.db import transaction

from accounts.enums import UserGroup
from accounts.utils import assign_user_to_group, has_group


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=UserGroup.choices, write_only=True, help_text='Role to assign to new user'
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')
        read_only_fields = ('id',)

    def validate_role(self, role):
        request = self.context.get('request')
        user = request.user if request else None

        if not user:
            raise serializers.ValidationError("Authentication required.")

        if user.is_superuser:
            return role

        if has_group(user, UserGroup.SUPER_ADMIN):
            if role in [UserGroup.SUPER_ADMIN.value, UserGroup.RESELLER_ADMIN.value, UserGroup.CLIENT_ADMIN.value]:
                return role

        elif has_group(user, UserGroup.RESELLER_ADMIN):
            if role == UserGroup.CLIENT_ADMIN.value:
                return role

        elif has_group(user, UserGroup.CLIENT_ADMIN):
            if role == UserGroup.BASE_USER.value:
                return role

        raise serializers.ValidationError(
            f"You don't have permission to create users with role '{role}'."
        )

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        assign_user_to_group(user, UserGroup(role))
        return user