# -*- coding: utf-8 -*-
"""Django settings for Guild project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

"""

from __future__ import absolute_import, unicode_literals
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['GUILD_DJANGO_SECRET_KEY']

ADMINS = (
    # ('Matt Austin', 'devops@mattaustin.com.au'),
    ('Elena Williams', 'elena@guild.house'),
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',


    'phonenumber_field',
    'raven.contrib.django.raven_compat',
    'robots',
    'sorl.thumbnail',
    'storages',
    'taggit',
    'tinymce',
    'sitetree',

    'project.menus',
    'project.admin',
    'project.blog',
    'project.library',
    'project.site',
    'project.bookings',
    'project.rolodex',
    'project.members',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.tz',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Canberra'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'Y-m-d'

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

MEDIA_URL = '/media/'

# Use Australian phone number format to store phone numbers
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'AU'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

STATIC_URL = '/static/'


# Sites framework

SITE_ID = 1


# Email

DEFAULT_FROM_EMAIL = 'hello@guild.house'

EMAIL_SUBJECT_PREFIX = '[Guild] '

SERVER_EMAIL = 'web@guild.house'

#BOOKINGS_TO_EMAILS = ['reservations@guild.house']
BOOKINGS_TO_EMAILS = ['web+testingserver@guild.house']

# Authentication

LOGIN_URL = '/admin/'


# Logging
# https://docs.getsentry.com/hosted/clients/python/integrations/django/#integration-with-logging

# LOGGING = {
# 'version': 1,
# 'disable_existing_loggers': True,
# 'root': {
# 'level': 'WARNING',
# 'handlers': ['sentry'],
# },
# 'formatters': {
# 'verbose': {
# 'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
##                       '%(thread)d %(message)s'
# },
# },
# 'handlers': {
# 'sentry': {
# 'level': 'ERROR',
# 'class':
# 'raven.contrib.django.raven_compat.handlers.SentryHandler',
# },
# 'console': {
# 'level': 'DEBUG',
# 'class': 'logging.StreamHandler',
# 'formatter': 'verbose'
# }
# },
# 'loggers': {
# 'django.db.backends': {
# 'level': 'ERROR',
# 'handlers': ['console'],
# 'propagate': False,
# },
# 'raven': {
# 'level': 'DEBUG',
# 'handlers': ['console'],
# 'propagate': False,
# },
# 'sentry.errors': {
# 'level': 'DEBUG',
# 'handlers': ['console'],
# 'propagate': False,
# },
# },
# }


# AWS

AWS_ACCESS_KEY_ID = ''  # TODO

AWS_SECRET_ACCESS_KEY = ''  # TODO
