# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .base import *  # NOQA
import warnings


DEBUG = True
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_DUMMY = False


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        # 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


# Email

DEFAULT_TO_EMAIL = 'web@guild.house'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_PORT = 1025


# Raven

RAVEN_CONFIG = {
    'dsn': 'http://1a37c19524264de189eef68c5fec2955:32e2c50d5a614bbf94e144b0c477732e@sentry.mattaustin.me.uk/10',  # NOQA
}


# Timezone warnings

warnings.filterwarnings(
    'error', r'DateTimeField received a naive datetime',
    RuntimeWarning, r'django\.db\.models\.fields')
