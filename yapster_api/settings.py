"""
Django settings for yapster_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gowp+a-x*u1(ff$s%wq%hqb##oxhdljr0bxhtrnxjwb9i24t25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
        BASE_DIR + '/templates/',
    )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'location',
    'users',
    'yap',
    'search',

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

ROOT_URLCONF = 'yapster_api.urls'

WSGI_APPLICATION = 'yapster_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": 'django.contrib.gis.db.backends.postgis',
        "HOST": "yte-1-db-1.cagmlb1zwzjw.us-east-1.rds.amazonaws.com",
        "PORT": "5432",
        "NAME": "yte_1_db_1",
        "USER": "yapster",
        "PASSWORD": "ABCD1234",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Email Configuration

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@yapster.co'
EMAIL_HOST_PASSWORD = 'Yapster1234'
DEFAULT_FROM_EMAIL = 'info@yapster.co'

#Push Production Notifications Configuration
#'''
APNS_USE_SANDBOX = True
APNS_CERT_FILE = '/home/ec2-user/api/yapsterapp_ios/yapster_ios_push_cert_dev.pem'
APNS_KEY_FILE = '/home/ec2-user/api/yapsterapp_ios/yapster_ios_push_key_dev.pem'
#'''

#Push Development Notification Configuration
'''
APNS_USE_SANDBOX = False
APNS_CERT_FILE = 'yapster_ios_push_cert.pem'
APNS_KEY_FILE = 'yapster_ios_push_key.pem'
#'''

#Facebook Configuration
FACEBOOK_APP_ID = '804473029570067'
FACEBOOK_APP_SECRET = '5188b2802c64fd3c2e3e47b152ba1d2b'

#Twitter Configuration
TWITTER_CONSUMER_KEY = 'XXhADNkyhY6mfCDmmNM5mBjbk'
TWITTER_CONSUMER_SECRET = '9mm3mnefi8BM0AXrPSxch8a3Xib4ryILXzxnzpnKoYMOWrYuNy'
TWITTER_ACCESS_TOKEN_KEY = '926669898-OuvLUVe8ZVlsGqdzZeNqKWfybwDAy1Mk6IuetxWi'
TWITTER_ACCESS_TOKEN_SECRET = 'LaQpcl5I1Y9pcQFfEXd2LylHE3uhRypYhsRqshzNbR2AL'

#AWS Boto Config
AWS_ACCESS_KEY_ID = 'AKIAJY5IOEVZFLTQNXNQ'
AWS_SECRET_ACCESS_KEY = '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'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_facebook.context_processors.facebook',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = BASE_DIR + '/static/'
