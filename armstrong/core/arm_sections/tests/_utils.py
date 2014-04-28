from armstrong.dev.tests.utils import ArmstrongTestCase, override_settings

from ..models import Section


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
            ('Weather', 'weather', 'All about weather', None)]
        for title, slug, summary, parent in data:
            if parent is not None:
                parent = self.sections[parent]
            self.sections.append(Section.objects.create(
                title=title,
                slug=slug,
                summary=summary,
                parent=parent))
