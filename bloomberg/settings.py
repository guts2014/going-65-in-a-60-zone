import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.getcwd()
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

STATIC_PATH = os.path.join(PROJECT_PATH,'static')
STATIC_URL = '/static/'


SECRET_KEY = 'c6d8+5xz0x3d0q21u@)@-ijkcf$il=*2ud$-u7vwbb7cnwsb!j'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bloomberg.urls'
WSGI_APPLICATION = 'bloomberg.wsgi.application'

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

STATICFILES_DIRS = (
	STATIC_PATH,
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
