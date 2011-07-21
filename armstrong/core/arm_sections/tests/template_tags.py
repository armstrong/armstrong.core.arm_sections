from ._utils import *
from ..models import Section
from ..templatetags import arm_sections
from django.core import urlresolvers
from django.template import Template, Context, TemplateSyntaxError

class SectionMenuTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(SectionMenuTestCase, self).setUp()
        self.sections = []
        data = [
                ('Local', 'local', 'All about local', None),
                ('Sports', 'sports', 'All about sports', None),
                ('College', 'college', 'All about college sports', 1),
                ('Pro', 'pro', 'All about pro sports', 1),
                ('Weather', 'weather', 'All about weather', None),
                ]
        for title, slug, summary, parent in data:
            if parent is not None:
                parent = self.sections[parent]
            self.sections.append(Section.objects.create(
                    title=title,
                    slug=slug,
                    summary=summary,
                    parent = parent,
                ))

    def wrap_in_resolve(self, val):
        result = fudge.Fake()
        result.provides('resolve').returns(val)
        return result

    def test_render_without_parameters(self):
        node = arm_sections.SectionMenuNode()
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
        node = arm_sections.SectionMenuNode(section_view="nonsense")
        with fudge.patched_context(urlresolvers, "reverse", reverse):
            result = node.render(None)
            for section in self.sections:
                section_link = "<a href='%s'>%s</a>" % (link, section.title) 
                self.assertTrue(section_link in result)

    def test_render_with_custom_template(self):
        node = arm_sections.SectionMenuNode(
                template=self.wrap_in_resolve('test_sections.html'))
        result = node.render(None)
        self.assertEquals(result, u'This is the test template\n')

    def test_render_with_node_subset(self):
        sports = self.sections[1]
        subset = Section.objects.filter(tree_id=sports.tree_id)
        subset = self.wrap_in_resolve(subset)
        node = arm_sections.SectionMenuNode(sections=subset)
        result = node.render(None)
        for section in self.sections:
            if section.tree_id == sports.tree_id:
                self.assertTrue(section.title in result)
            else:
                self.assertFalse(section.title in result)

    def test_section_menu_parser_empty(self):
        template = Template("""{% load arm_sections %}
                {% section_menu %}""")
        section_node = template.nodelist[2]
        all_sections = Section.objects.all().order_by('tree_id')
        self.assertEquals(section_node.__class__, arm_sections.SectionMenuNode)
        self.assertEquals(section_node.sections, None)
        self.assertEquals(section_node.section_view, None)
        self.assertEquals(section_node.template, None)

    def test_section_menu_parser_template(self):
        template = Template("""{% load arm_sections %}
                {% section_menu template='FOO/BAR/BAZ.html' %}""")
        section_node = template.nodelist[2]
        self.assertEquals(section_node.template.resolve({}),
                'FOO/BAR/BAZ.html')

    def test_render_from_template_with_custom_template(self):
        template = Template('{% load arm_sections %}' + \
                '{% section_menu template="test_sections.html" %}')
        result = template.render(Context({}))
        self.assertEquals(result, u'This is the test template\n')

    def test_section_menu_parser_invalid(self):
        with self.assertRaises(TemplateSyntaxError):
            template = Template('{% load arm_sections %}' + \
                    '{% section_menu "test_sections.html" %}')
