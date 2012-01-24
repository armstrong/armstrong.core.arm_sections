from django.contrib import admin
from django.conf.urls.defaults import *

from armstrong.core.arm_sections.views import SimpleSectionView, SectionFeed

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sections/(?P<full_slug>([\w\-\_]+/)+)$',
        SimpleSectionView.as_view(template_name='test_sections.html'),
        name='section_detail'),
    url(r'^feeds/sections/(?P<full_slug>([\w\-\_]+/)+)$',
        SectionFeed(section_view='section_detail'),
        name='section_feed'),
)
