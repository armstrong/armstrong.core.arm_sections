from django.contrib import admin
try:
    from django.conf.urls import patterns, include, url
except ImportError:  # Django 1.3 # pragma: no cover
    from django.conf.urls.defaults import patterns, include, url

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

# for shell & runserver: Django 1.3 and 1.4 don't need this, but 1.5 does
# it will only work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
