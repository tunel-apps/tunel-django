import os
import tempfile
import yaml
import sys

from django.core.management.utils import get_random_secret_key
from datetime import datetime
from importlib import import_module

# Build paths inside the project with the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

# The spackmon global conflict contains all settings.
SETTINGS_FILE = os.environ.get('TUNELDJANGO_SETTINGS_FILE') or os.path.join(ROOT_DIR, "settings.yaml")
if not os.path.exists(SETTINGS_FILE):
    sys.exit("Global settings file settings.yaml is missing in the install directory.")

# Read in the settings file to get settings
class Settings:
    """
    convert a dictionary of settings (from yaml) into a class
    """

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
        setattr(self, "UPDATED_AT", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

    def __str__(self):
        return "[tunel-django-settings]"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value


with open(SETTINGS_FILE, "r") as fd:
    cfg = Settings(yaml.load(fd.read(), Loader=yaml.FullLoader))

# For each setting, if it's defined in the environment with spackmon_ prefix, override
for key, value in cfg:
    envar = os.getenv("TUNELDJANGO_%s" % key)

    # Note that empty envars can be empty strings
    if envar is not None:
        setattr(cfg, key, envar)

# Secret Key and Dates


def generate_secret_keys(filename):
    """
    A helper function to write a randomly generated secret key to file
    """
    with open(filename, "w") as fd:
        for keyname in ["SECRET_KEY", "JWT_SERVER_SECRET"]:
            key = get_random_secret_key()
            fd.writelines("%s = '%s'\n" % (keyname, key))

# Generate secret keys if do not exist, and not defined in environment
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SERVER_SECRET = os.environ.get("JWT_SERVER_SECRET")

if not SECRET_KEY or not JWT_SERVER_SECRET:
    try:
        from .secret_key import SECRET_KEY, JWT_SERVER_SECRET
    except ImportError:
        generate_secret_keys(os.path.join(BASE_DIR, "secret_key.py"))
        from .secret_key import SECRET_KEY, JWT_SERVER_SECRET

# Set the domain name (and keep record of without port)
DOMAIN_NAME = cfg.DOMAIN_NAME
DOMAIN_NAME_PORTLESS = cfg.DOMAIN_NAME
if cfg.DOMAIN_PORT:
    DOMAIN_NAME = "%s:%s" % (DOMAIN_NAME, cfg.DOMAIN_PORT)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = cfg.DOMAIN_NAME


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == "true" else False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Title for the website
TITLE = os.environ.get("TUNELDJANGO_TITLE", "tunel-django")
AUTHOR = os.environ.get("AUTHOR", "vsoch")
KEYWORDS = os.environ.get("KEYWORDS", "django,template")

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "http://127.0.0.1")
SOCIAL_AUTH_LOGIN_REDIRECT_URL = DOMAIN_NAME

# Custom user model
AUTH_USER_MODEL = "users.User"

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/2.1/ref/settings/
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "tuneldjango.apps.base",
    "tuneldjango.apps.main",
    "tuneldjango.apps.users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    'django.contrib.staticfiles',
    "django.contrib.messages",
    "django_extensions",
    "django_gravatar",
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

ROOT_URLCONF = "tuneldjango.urls"

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

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
WSGI_APPLICATION = "tuneldjango.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Install PyMySQL as mysqlclient/MySQLdb to use Django's mysqlclient adapter
# See https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-db-api-drivers
# for more information
import pymysql  # noqa: 402

pymysql.version_info = (1, 4, 6, "final", 0)  # change mysqlclient version
pymysql.install_as_MySQLdb()

if os.getenv("MYSQL_HOST") is not None:
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.environ.get("MYSQL_HOST"),
            "USER": os.environ.get("MYSQL_USER"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD"),
            "NAME": os.environ.get("MYSQL_DATABASE"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }
else:
    # Use sqlite when testing locally
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: 501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '/var/www/static/')
MEDIA_URL = 'data/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '/var/www/data/')

# Caches

# POSTs to API typically have a limit of 2.5MB, disable limit
DATA_UPLOAD_MAX_MEMORY_SIZE = None

# Disable check for max memory size of data
DATA_UPLOAD_MAX_MEMORY_SIZE = None
FILE_UPLOAD_MAX_MEMORY_SIZE = None

# Logging

# Default Django logging is WARNINGS+ to console
# so visible via docker-compose logs uwsgi
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": cfg.LOG_LEVEL,
        },
    },
}

if cfg.ENABLE_SENTRY:

    SENTRY_DSN = cfg.SENTRY_DSN
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=cfg.SENTRY_DSN, integrations=[DjangoIntegration()])

# Rate Limiting

# Set to very high values to allow for development, etc.
VIEW_RATE_LIMIT = "1000/1d"  # The rate limit for each view, django-ratelimit, "50 per day per ipaddress)
VIEW_RATE_LIMIT_BLOCK = (
    True  # Given that someone goes over, are they blocked for the period?
)

# On any admin or plugin login redirect to standard social-auth entry point for agreement to terms
LOGIN_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

## API #########################################################################

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    # You can require authentication for your API
    # Be careful adding this - endpoints for the front page table won't work
    #'DEFAULT_PERMISSION_CLASSES': (
    #    'rest_framework.permissions.IsAuthenticated',
    # ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    # You can also customize the throttle rates, for anon and users
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.AnonRateThrottle",),
    # https://www.django-rest-framework.org/api-guide/throttling/
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
    },
    "PAGE_SIZE": 10,
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": ["internal_apis"],  #  List URL namespaces to ignore
}

API_VERSION = "v1"
