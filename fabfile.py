from armstrong.dev.tasks import *
from fabric.api import task


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'armstrong.core.arm_sections',
        'armstrong.core.arm_sections.tests.arm_sections_support',
        'south',
        'mptt',
    ),
    'STATIC_URL': '/static/',
    'ROOT_URLCONF': 'armstrong.core.arm_sections.tests.arm_sections_support.urls',
    'ARMSTRONG_SECTION_ITEM_MODEL': 'armstrong.core.arm_sections.tests.arm_sections_support.models.SimpleCommon',
}

full_name = "armstrong.core.arm_sections"
main_app = "arm_sections"
tested_apps = (main_app, )
pip_install_first = True
