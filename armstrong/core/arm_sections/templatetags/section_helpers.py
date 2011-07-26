from ..models import Section
from django.utils.safestring import mark_safe as _
from django import template as djtemplate
from django.template.loader import render_to_string
from django.template.defaulttags import token_kwargs

register = djtemplate.Library()


class SectionMenuNode(djtemplate.Node):
    def __init__(self,
            template=None,
            section_view=None,
            sections=None):
        self.template = template
        self.section_view = section_view
        self.sections = sections

    def render(self, context):
        if self.template is None:
            template = 'arm_sections/sections_menu.html'
        else:
            template = self.template.resolve(context)

        if self.sections is None:
            sections = Section.objects.all().order_by('tree_id')
        else:
            sections = self.sections.resolve(context)

        dictionary = {'sections': sections,
                      'section_view': self.section_view,
                     }
        return render_to_string(template, dictionary=dictionary)


@register.tag(name='section_menu')
def do_section_menu(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        args = token.split_contents()[1:]
        kwargs = token_kwargs(args, parser)
        if len(args) > 0:
            raise ValueError
    except ValueError:
        raise djtemplate.TemplateSyntaxError(
                "%r tag accepts only keyword arguments" \
                % token.contents.split()[0])
    return SectionMenuNode(**kwargs)
