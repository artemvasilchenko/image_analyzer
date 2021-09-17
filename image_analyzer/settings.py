"""Django settings for image_analyzer project."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = os.environ

SECRET_KEY = env.get('SECRET_KEY', 'your_secret_key')

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'app_image_analyzer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'image_analyzer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'image_analyzer.wsgi.application'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'json',
            'level': 'INFO',
        },
    },
    'formatters': {
        'json': {
            '()': 'json_log_formatter.JSONFormatter',
        },
    },
    'loggers': {
        'app_image_analyzer.views': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}
