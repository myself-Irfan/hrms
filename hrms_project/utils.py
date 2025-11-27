from django.core.exceptions import ImproperlyConfigured
import os

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise ImproperlyConfigured(f"Environment variable '{var_name}' not set in .env")
    return value
