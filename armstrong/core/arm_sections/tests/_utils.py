from datetime import datetime
from django.core.files import File
from django.conf import settings

from armstrong.dev.tests.utils import ArmstrongTestCase
from armstrong.dev.tests.utils.backports import *
from armstrong.dev.tests.utils.concrete import *
from armstrong.dev.tests.utils.users import *

from ..models import Section

import fudge


class ArmSectionsTestCase(ArmstrongTestCase):
    def setUp(self):
        super(ArmSectionsTestCase, self).setUp()
        self.sections = []
        data = [
                ('Local', 'local', 'All about local', None),
                ('Sports', 'sports', 'All about sports', None),
                ('College', 'college', 'All about college sports', 1),
                ('Pro', 'pro', 'All about pro sports', 1),
                ('US', 'us', 'All about US sports', 3),
                ('Weather', 'weather', 'All about weather', None),
                ]
        for title, slug, summary, parent in data:
            if parent is not None:
                parent = self.sections[parent]
            self.sections.append(Section.objects.create(
                    title=title,
                    slug=slug,
                    summary=summary,
                    parent=parent,
                ))
