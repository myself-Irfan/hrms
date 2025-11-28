from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from accounts.enums import UserGroup


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Optional')
    user_group = forms.ChoiceField(
        choices=UserGroup.choices,
        required=True,
        label='User Group',
        help_text='Select the group for this user'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })
        self.fields['user_group'].widget.attrs.update({
            'placeholder': 'Select User Group'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })

        self._ensure_groups_exist()

    @staticmethod
    def _ensure_groups_exist():
        """Create groups if they don't exist"""
        for group_value, group_label in UserGroup.choices:
            Group.objects.get_or_create(name=group_value)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')

        if commit:
            user.save()
            group_name = self.cleaned_data['user_group']
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user