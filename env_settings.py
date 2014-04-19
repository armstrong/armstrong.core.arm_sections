from armstrong.dev.default_settings import *


INSTALLED_APPS.extend([
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'mptt',
    'armstrong.core.arm_sections.tests.arm_sections_support'])

STATIC_URL = "/static/"
ROOT_URLCONF = 'armstrong.core.arm_sections.tests.arm_sections_support.urls'
ARMSTRONG_SECTION_ITEM_MODEL = \
    'armstrong.core.arm_sections.tests.arm_sections_support.models.SimpleCommon'
