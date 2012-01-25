from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from .models import Section


class SimpleSectionView(DetailView):
    context_object_name = 'section'
    model = Section

    def get_object(self):
        return self.get_section()

    def get_section(self):
        return get_object_or_404(self.get_queryset(),
                                 full_slug=self.kwargs['full_slug'])


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
