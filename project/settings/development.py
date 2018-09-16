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


# Timezone warnings

warnings.filterwarnings(
    'error', r'DateTimeField received a naive datetime',
    RuntimeWarning, r'django\.db\.models\.fields')

MEDIA_ROOT = os.path.join(BASE_DIR, "public/media")  # noqa
