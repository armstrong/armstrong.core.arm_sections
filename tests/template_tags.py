import fudge
from django.conf import settings
from django.core import urlresolvers
from django.template import (
    Template, Context, TemplateDoesNotExist, TemplateSyntaxError)

from armstrong.core.arm_sections.models import Section
from ._utils import ArmSectionsTestCase


class SectionMenuTestCase(ArmSectionsTestCase):
    def setUp(self):
        self.string = ""
        self.context = Context()

    def tearDown(self):
        # Clear the cached template between test runs
        if hasattr(self, '_rendered_template'):
            del self._rendered_template

    @classmethod
    def setUpClass(cls):
        """Set Template settings to known values"""
        cls.old_td, settings.TEMPLATE_DEBUG = settings.TEMPLATE_DEBUG, False

    @classmethod
    def tearDownClass(cls):
        settings.TEMPLATE_DEBUG = cls.old_td

    @property
    def rendered_template(self):
        """Cache the rendered template result during a test run"""
        if not hasattr(self, '_rendered_template'):  # pragma: no cover
            template = "{% load section_helpers %}" + self.string
            self._rendered_template = Template(template).render(self.context)
        return self._rendered_template

    def test_render_without_parameters(self):
        self.string = '{% section_menu %}'
        self.assertNotIn("<a href", self.rendered_template)
        for section in Section.objects.all():
            self.assertIn(section.title, self.rendered_template)

    def test_tag_only_accepts_kwargs(self):
        err = "accepts only keyword arguments"
        self.string = '{% section_menu "will break" %}'
        with self.assertRaisesRegexp(TemplateSyntaxError, err):
            self.rendered_template

    def test_render_with_custom_template(self):
        self.string = '{% section_menu template="test_sections.html" %}'
        self.assertNotIn("<a href", self.rendered_template)
        self.assertEqual(u'This is the test template\n', self.rendered_template)

    def test_missing_custom_template_raises_error(self):
        self.string = '{% section_menu template="FOO/BAR/BAZ.html" %}'
        with self.assertRaises(TemplateDoesNotExist):
            self.rendered_template

    def test_render_with_section_view(self):
        reverse = fudge.Fake()
        link = "/link/to/section"
        reverse.is_callable().returns(link)
        self.string = '{% section_menu section_view="nonsense" %}'

        with fudge.patched_context(urlresolvers, "reverse", reverse):
            for section in Section.objects.all():
                section_link = "<a href='%s'>%s</a>" % (link, section.title)
                self.assertIn(section_link, self.rendered_template)

    def test_section_view_must_be_in_urlconf(self):
        self.string = '{% section_menu section_view="nonsense" %}'
        with self.assertRaises(urlresolvers.NoReverseMatch):
            self.rendered_template

    def test_render_with_sections_subset(self):
        subset = Section.objects.filter(full_slug__startswith="sports")
        self.context['subset'] = subset
        self.string = '{% section_menu sections=subset %}'

        for section in Section.objects.all():
            if section in subset:
                self.assertIn(section.title, self.rendered_template)
            else:
                self.assertNotIn(section.title, self.rendered_template)

    def test_subsections_nest_properly(self):
        subset = Section.objects.filter(full_slug__startswith="sports")
        self.context['subset'] = subset
        self.string = '{% section_menu sections=subset %}'

        occurrences = self.rendered_template.count('<ul class="children">')
        self.assertEqual(occurrences, 2)

    def test_empty_sections_yields_empty_list(self):
        self.context['subset'] = []
        self.string = '{% section_menu sections=subset %}'
        self.assertNotIn("<li>", self.rendered_template)
