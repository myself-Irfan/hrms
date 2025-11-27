from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

from hrms_project.utils import get_env_variable
from hrms_project.logging_config import get_logger_config, configure_structlog


BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / '.env'

if not DOTENV_PATH.exists():
    raise ImproperlyConfigured('.env file not found. Did you forget to add one?')

load_dotenv(DOTENV_PATH, verbose=True, override=True, encoding='utf-8')

SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = get_env_variable('DEBUG').upper() == 'TRUE'
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    
    # Local apps
    'accounts',
    'tenants',
    'employees',
    'attendance',
    'leave',
    'payroll',
    'notices',
    'expenses',
    'reports',
    'mobile_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hrms_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hrms_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path={}'.format(get_env_variable('DEFAULT_DB_SCHEMA'))
        },
        'NAME': get_env_variable('DEFAULT_DB_NAME'),
        'USER': get_env_variable('DEFAULT_DB_USER'),
        'PASSWORD': get_env_variable('DEFAULT_DB_PWD'),
        'HOST': get_env_variable('DEFAULT_DB_HOST'),
        'PORT': get_env_variable('DEFAULT_DB_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(get_env_variable('ACCESS_TOKEN_LIFETIME_IN_MIN'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(get_env_variable('REFRESH_TOKEN_LIFETIME_IN_MIN'))),
}

# logging config

LOG_DIR = BASE_DIR / get_env_variable("LOG_DIR")
LOG_DIR.mkdir(parents=True, exist_ok=True)
BACKEND_LOG_FILE_NAME = get_env_variable("BACKEND_LOG_FILE_NAME")
LOG_LEVEL = get_env_variable("LOG_LVL").upper()
DISABLED_FIELDS_TO_LOG = [
    f.strip() for f in get_env_variable("DISABLED_FIELDS_TO_LOG").split(",") if f.strip(",")
]

LOGGING = get_logger_config()
configure_structlog()