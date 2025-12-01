from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Invalid username or password. Please try again."
        ),
        'inactive': (
            "This account has been deactivated. Please contact support."
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True,
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })

        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'