from armstrong.dev.tasks import *
from fabric.api import task


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'armstrong.core.arm_sections',
        'armstrong.core.arm_sections.tests.arm_sections_support',
        'lettuce.django',
        'south',
        'mptt',
    ),
    'ROOT_URLCONF': 'armstrong.core.arm_sections.tests.arm_sections_support.urls',
    'SITE_ID': 1,
    'ARMSTRONG_SECTION_ITEM_MODEL': 'armstrong.core.arm_sections.tests.arm_sections_support.models.SimpleCommon',
}

full_name = "armstrong.core.arm_sections"
main_app = "arm_sections"
tested_apps = (main_app, )
pip_install_first = True
