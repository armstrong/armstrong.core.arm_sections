from armstrong.dev.default_settings import *


INSTALLED_APPS.extend([
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'mptt',
    'tests.arm_sections_support'])

STATIC_URL = "/static/"
ROOT_URLCONF = 'tests.arm_sections_support.urls'
ARMSTRONG_SECTION_ITEM_MODEL = 'tests.arm_sections_support.models.SimpleCommon'
