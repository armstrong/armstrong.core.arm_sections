from armstrong.dev.default_settings import *


INSTALLED_APPS.extend([
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'mptt',
    'tests.support'])

STATIC_URL = "/static/"
ROOT_URLCONF = 'tests.support.urls'
ARMSTRONG_SECTION_ITEM_MODEL = 'tests.support.models.SimpleCommon'
