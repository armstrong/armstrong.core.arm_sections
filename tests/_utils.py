from armstrong.dev.tests.utils import ArmstrongTestCase, override_settings
from armstrong.core.arm_sections.models import Section


class ArmSectionsTestCase(ArmstrongTestCase):
    fixtures = ['test_sections']

    def setUp(self):
        super(ArmSectionsTestCase, self).setUp()
        self.sections = Section.objects.all()
