from django.contrib import admin
from django.conf.urls.defaults import *

from armstrong.core.arm_sections.views import SimpleSectionView, SectionFeed

from .models import CustomSection
from .views import CustomSectionView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sections/(?P<full_slug>([\w\-\_]+/)+)$',
        SimpleSectionView.as_view(template_name='test_sections.html'),
        name='section_detail'),
    url(r'^feeds/sections/(?P<full_slug>([\w\-\_]+/)+)$',
        SectionFeed(section_view='section_detail'),
        name='section_feed'),
    url(r'^custom-sections/(?P<full_slug>([\w\-\_]+/)+)$',
        SimpleSectionView.as_view(template_name='test_sections.html',
                                  model=CustomSection),
        name='custom_section_detail'),
    url(r'^custom-sections-queryset/(?P<full_slug>([\w\-\_]+/)+)$',
        CustomSectionView.as_view(template_name='test_sections.html'),
        name='custom_section_queryset_detail'),
)
