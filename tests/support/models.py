import django
from django.db import models
from model_utils.managers import InheritanceManager

from armstrong.core.arm_sections.managers import SectionSlugManager
from armstrong.core.arm_sections.models import Section


PUB_STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published'),
)


class PublishedManager(InheritanceManager):
    def get_queryset(self):  # DROP_WITH_DJANGO15
        method = 'get_query_set' if django.VERSION < (1, 6) else 'get_queryset'
        return getattr(super(PublishedManager, self), method)()\
            .filter(pub_status="P")

    if django.VERSION < (1, 6):  # DROP_WITH_DJANGO15
        get_query_set = get_queryset


class Common(models.Model):
    title = models.CharField(max_length=20)
    sections = models.ManyToManyField(Section)
    slug = models.SlugField()
    pub_status = models.CharField(max_length=1, choices=PUB_STATUS_CHOICES)

    objects = InheritanceManager()
    published = PublishedManager()
    with_section = SectionSlugManager(section_field="sections")

    class Meta:
        app_label = 'support'


class Article(Common):
    summary = models.TextField(default="Default", blank=True)

    class Meta:
        app_label = 'support'


class SimpleCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    slug = models.SlugField()

    objects = models.Manager()
    with_section = SectionSlugManager()

    class Meta:
        app_label = 'support'


class SimpleArticle(SimpleCommon):
    summary = models.TextField(default="Default", blank=True)

    class Meta:
        app_label = 'support'


class NonStandardField(models.Model):
    title = models.CharField(max_length=20)
    sections_by_another_name = models.ForeignKey(Section)
    slugs_by_another_name = models.SlugField()

    objects = models.Manager()
    with_section = SectionSlugManager(
        section_field="sections_by_another_name",
        slug_field="slugs_by_another_name")

    class Meta:
        app_label = 'support'


class SectionForeignKeyCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    slug = models.SlugField()

    objects = InheritanceManager()
    with_section = SectionSlugManager()

    class Meta:
        app_label = 'support'


class SectionForeignKeyArticle(SectionForeignKeyCommon):
    summary = models.TextField(default="Default", blank=True)

    class Meta:
        app_label = 'support'


class ComplexCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    related_sections = models.ManyToManyField(
        Section, related_name='relatedcomplexcommon_set')
    slug = models.SlugField()

    objects = InheritanceManager()
    with_section = SectionSlugManager()

    class Meta:
        app_label = 'support'


class ComplexArticle(ComplexCommon):
    summary = models.TextField(default="Default", blank=True)

    class Meta:
        app_label = 'support'


class CustomSection(Section):
    class Meta:
        app_label = 'support'


class MultipleManyToManyModel(ComplexCommon):
    more_sections = models.ManyToManyField(
        Section, related_name='moresections_set')

    class Meta:
        app_label = 'support'
