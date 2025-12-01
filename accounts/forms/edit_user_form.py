from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import ClientLicenseInfo


class EditUserForm(forms.Form):
    first_name = forms.CharField(label="First Name", required=False, max_length=150)
    last_name = forms.CharField(label="Last Name", required=False, max_length=150)
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(
        label="New Password (leave blank to keep current)",
        widget=forms.PasswordInput,
        required=False
    )
    password_confirm = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False
    )
    license_count = forms.IntegerField(
        label="License Count",
        required=False,
        min_value=0,
        help_text="Only applicable for Reseller Admin and Client Admin"
    )
    is_active = forms.BooleanField(
        label="Active",
        required=False,
        help_text="Uncheck to deactivate the user account"
    )

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            self.fields['is_active'].initial = self.user_instance.is_active

            try:
                license_info = self.user_instance.license_info
                self.fields['license_count'].initial = license_info.total_licenses
                self.fields['license_count'].help_text = (
                    f"Currently using {license_info.used_licenses} licenses. "
                    f"Must be >= {license_info.used_licenses}"
                )
            except ClientLicenseInfo.DoesNotExist:
                self.fields['license_count'].widget = forms.HiddenInput()

        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs.update({'class': 'form-check-input'})
            elif not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.user_instance:
            if User.objects.filter(email=email).exclude(id=self.user_instance.id).exists():
                raise ValidationError("This email is already in use by another user.")
        return email

    def clean_license_count(self):
        license_count = self.cleaned_data.get('license_count')

        if license_count is not None and self.user_instance:
            try:
                license_info = self.user_instance.license_info
                if license_count < license_info.used_licenses:
                    raise ValidationError(
                        f"License count cannot be less than currently used licenses "
                        f"({license_info.used_licenses})."
                    )
            except ClientLicenseInfo.DoesNotExist:
                pass

        return license_count

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data