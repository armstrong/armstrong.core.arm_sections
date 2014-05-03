import fudge
from django.core import urlresolvers
from django.template import Template, Context, TemplateSyntaxError

from armstrong.core.arm_sections.models import Section
from armstrong.core.arm_sections.templatetags import section_helpers

from ._utils import ArmSectionsTestCase


def generate_stub_resolve(val):
    result = fudge.Fake()
    result.provides('resolve').returns(val)
    return result


class SectionMenuTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(SectionMenuTestCase, self).setUp()

    def test_render_without_parameters(self):
        node = section_helpers.SectionMenuNode()
        result = node.render(None)
        for section in self.sections:
            self.assertTrue(section.title in result)
            self.assertFalse("<a href" in result)

    def test_render_with_section_view(self):
        reverse = fudge.Fake()
        link = "/link/to/section"
        reverse.is_callable().returns(link)
        # section_view doesn't need to be wrapped, because the value is passed
        # unchanged to the url tag which does the right thing regardless
        node = section_helpers.SectionMenuNode(section_view="nonsense")
        with fudge.patched_context(urlresolvers, "reverse", reverse):
            result = node.render(None)
            for section in self.sections:
                section_link = "<a href='%s'>%s</a>" % (link, section.title)
                self.assertTrue(section_link in result)

    def test_render_with_custom_template(self):
        node = section_helpers.SectionMenuNode(
            template=generate_stub_resolve('test_sections.html'))
        result = node.render(None)
        self.assertEqual(result, u'This is the test template\n')

    def test_render_with_node_subset(self):
        sports = self.sections[1]
        subset = Section.objects.filter(tree_id=sports.tree_id)
        subset = generate_stub_resolve(subset)
        node = section_helpers.SectionMenuNode(sections=subset)
        result = node.render(None)
        for section in self.sections:
            if section.tree_id == sports.tree_id:
                self.assertTrue(section.title in result)
            else:
                self.assertFalse(section.title in result)

    def test_section_menu_parser_empty(self):
        template = Template(
            '{% load section_helpers %}' +
            '{% section_menu %}')
        section_node = template.nodelist[1]
        Section.objects.all().order_by('tree_id')
        self.assertIsInstance(section_node, section_helpers.SectionMenuNode)
        self.assertIsNone(section_node.sections)
        self.assertIsNone(section_node.section_view)
        self.assertIsNone(section_node.template)

    def test_section_menu_parser_template(self):
        template = Template(
            '{% load section_helpers %}' +
            '{% section_menu template="FOO/BAR/BAZ.html" %}')
        section_node = template.nodelist[1]
        self.assertEqual(
            section_node.template.resolve({}),
            'FOO/BAR/BAZ.html')

    def test_render_from_template_with_custom_template(self):
        template = Template(
            '{% load section_helpers %}' +
            '{% section_menu template="test_sections.html" %}')
        result = template.render(Context({}))
        self.assertEqual(result, u'This is the test template\n')

    def test_section_menu_parser_invalid(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(
                '{% load section_helpers %}' +
                '{% section_menu "test_sections.html" %}')
