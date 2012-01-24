from ._utils import *
from ..models import Section
from ..templatetags import section_helpers
from django.core import urlresolvers
from django.template import Template, Context, TemplateSyntaxError


class SectionsViewTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(SectionsViewTestCase, self).setUp()
        self.sports = Section.objects.get(slug='sports')

    def test_view_responds_to_full_slug_url(self):
        url = urlresolvers.reverse(
                'section_detail', kwargs={'full_slug': self.sports.full_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_for_missing_section_raises_404(self):
        url = urlresolvers.reverse(
                'section_detail', kwargs={'full_slug': 'not-a-section/nope/'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
