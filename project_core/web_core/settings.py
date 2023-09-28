# Utils
import os
from pathlib import Path

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-nz75^065j590+*f$!4b6y9&jn=m%6mp5jynzu3%etf)zv8$w&y'
SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET')
DEBUG = os.getenv('DEBUG', default=True)

ALLOWED_HOSTS = ['*',]
INTERNAL_IPS = ['127.0.0.1',]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

PROJECT_APP = [
    'apps.dogma_infoseq.apps.DogmaInfoseqConfig',
    'apps.dogma_it.apps.DogmaItConfig',
    'apps.dogma_users.apps.DogmaUsersConfig',
]

INSTALLED_APPS += (PROJECT_APP)

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


ROOT_URLCONF = 'web_core.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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


WSGI_APPLICATION = 'web_core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# IfoSeq storage
INFOSEQ_URL = 'infoseq_storage/'
INFOSEQ_ROOT = os.path.join(BASE_DIR, 'infoseq_storage')
PLATFORM_USER = os.getenv('PLATFORM_USER')
NET_CORE = os.getenv('PLATFORM_USER')
VPN_SERVER = os.getenv('VPN_SERVER')
VPN_PORT= os.getenv('VPN_PORT')


# It storage
ITSTORAGE_URL = 'it_storage/'
ITSTORAGE_ROOT = os.path.join(BASE_DIR, 'it_storage')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'dogma_users.DogmaUser'


# DiscordSettings
DISCORD_ADMINISTROTUMSERVITOR = os.getenv('DISCORD_ADMINISTROTUMSERVITOR')
DISCORD_1LINE_SERVITOR = os.getenv('DISCORD_1LINE_SERVITOR')
DISCORD_ASTRONOMIKON_SERVITOR = os.getenv('DISCORD_ASTRONOMIKON_SERVITOR')
DISCORD_WARP_SERVITOR = os.getenv('DISCORD_WARP_SERVITOR')

