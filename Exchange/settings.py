"""
Django settings for Exchange project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import uuid
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%p*m%z8z)jxkgvt1b0m)ha=e$uexa$i5o5-tifc=-t#9%7p+gg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = '/api/1.0/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'assets')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SENDER = '84e847f929d34f66a94bf376cf30d12c'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

# Application definition

INSTALLED_APPS = (
    'sslserver',
    'flat',
    'activelink',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'incidents',
    'sending',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'widget_tweaks',
    'datetimewidget',
    'bootstrap_pagination',
    'a_ppl_e',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'Exchange', 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'Exchange.urls'

WSGI_APPLICATION = 'Exchange.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# RestFramework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
    'PAGINATE_BY': 10,
    
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'subscriber': 'Subscriber', 'provider': 'Provider'}
}


CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:8800',
)

OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'


# TLP
TLP_SCHEME = 'enisa' # US-CERT or ENISA
TLP_DEFAULT_VALUE = 'green' # red, amber, green or white