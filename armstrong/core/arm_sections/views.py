from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed

from .models import Section


class SimpleSectionView(TemplateView):
    well_title = None

    def get_section(self):
        return Section.objects.get(full_slug=self.kwargs['full_slug'])

    def get_context_data(self, **kwargs):
        context = super(SimpleSectionView, self).get_context_data(**kwargs)
        context["section"] = self.get_section()
        return context


class SectionFeed(Feed):
    def __init__(self, section_view, *args, **kwargs):
        self.section_view = section_view

    def get_object(self, request, full_slug):
        return Section.objects.get(full_slug=full_slug)

    def title(self, section):
        return section.title

    def link(self, section):
        return reverse(self.section_view,
                kwargs={'full_slug': section.full_slug})

    def description(self, section):
        return section.summary

    def items(self, section):
        return section.items
