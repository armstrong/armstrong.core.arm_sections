from django.core import urlresolvers

from ._utils import ArmSectionsTestCase
from ..models import Section
from .arm_sections_support.models import CustomSection


class SectionsViewTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(SectionsViewTestCase, self).setUp()
        self.sports = Section.objects.get(slug='sports')
        self.us_pro_sports = Section.objects.get(full_slug='sports/pro/us')
        self.custom_section = CustomSection.objects.create(
                    title='Custom',
                    slug='custom',
                    summary='Custom section',
                    parent=None,
                )

    def test_view_responds_to_full_slug(self):
        url = urlresolvers.reverse(
                'section_detail',
                kwargs={'full_slug': self.sports.full_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url = urlresolvers.reverse(
                'section_detail',
                kwargs={'full_slug': self.us_pro_sports.full_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_has_section_in_context(self):
        url = urlresolvers.reverse(
                'section_detail',
                kwargs={'full_slug': self.sports.full_slug})
        response = self.client.get(url)
        self.assertEqual(response.context['section'], self.sports)

    def test_view_with_custom_section_model(self):
        url = urlresolvers.reverse(
                'custom_section_detail',
                kwargs={'full_slug': self.custom_section.full_slug})
        response = self.client.get(url)
        base_section = Section.objects.get(id=self.custom_section.id)
        self.assertEqual(response.context['section'], self.custom_section)
        self.assertNotEqual(response.context['section'], base_section)

    def test_view_for_missing_section_raises_404(self):
        url = urlresolvers.reverse(
                'section_detail',
                kwargs={'full_slug': 'not-a-section/nope/'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_feed_view(self):
        url = urlresolvers.reverse(
                'section_feed',
                kwargs={'full_slug': self.us_pro_sports.full_slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_feed_view_for_missing_section_raises_404(self):
        url = urlresolvers.reverse(
                'section_feed',
                kwargs={'full_slug': 'not-a-section/nope/'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_view_with_custom_queryset(self):
        url = urlresolvers.reverse(
                'custom_section_queryset_detail',
                kwargs={'full_slug': self.custom_section.full_slug})
        response = self.client.get(url)
        base_section = Section.objects.get(id=self.custom_section.id)
        self.assertEqual(response.context['section'], self.custom_section)
        self.assertNotEqual(response.context['section'], base_section)
