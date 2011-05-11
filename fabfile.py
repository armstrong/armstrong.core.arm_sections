from armstrong.dev.tasks import *
from d51.django.virtualenv.base import VirtualEnvironment
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
        'lettuce.django',
        'south',
    ),
    'SITE_ID': 1,
}

main_app = "arm_sections"
tested_apps = (main_app, )

@task
def lettuce(verbosity=4):
    v.run(settings)
    v.call_command("harvest", apps='armstrong.core.arm_sections',
            verbosity=verbosity)
