from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.create_user_service import UserCreateService
from accounts.enums import UserGroup


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    email = forms.EmailField(label="Email", required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    user_group = forms.ChoiceField(label="User Group", required=True)
    license_count = forms.IntegerField(label="License Count", required=False, min_value=1)

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        UserCreateService.ensure_groups_exist()
        self.allowed_groups = UserCreateService.get_allowed_groups(self.current_user)
        self.fields['user_group'].choices = [
            ("", "Select User Group"),
            *[(g.value, g.label) for g in self.allowed_groups]
        ]

        # Dynamic placeholders
        for field_name, field in self.fields.items():
            placeholder = f"Select {field.label}" if isinstance(field, forms.ChoiceField) else field.label
            field.widget.attrs.update({'placeholder': placeholder})

    def clean_user_group(self):
        group_name = self.cleaned_data['user_group']
        if not group_name:
            raise ValidationError("Please select a user group.")
        if group_name not in self.allowed_groups:
            raise ValidationError("You cannot assign this group.")
        return group_name

    def clean_license_count(self):
        group_name = (self.cleaned_data.get('user_group') or "").lower()
        license_count = self.cleaned_data.get('license_count')

        if group_name in [UserGroup.CLIENT_ADMIN.value, UserGroup.RESELLER_ADMIN.value] and not license_count:
            raise ValidationError("License count is required for this user group.")

        return license_count

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError("Passwords do not match.")
        return cleaned_data