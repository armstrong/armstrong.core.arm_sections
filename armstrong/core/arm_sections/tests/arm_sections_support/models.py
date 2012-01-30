from armstrong.core.arm_sections.managers import SectionSlugManager
from armstrong.core.arm_sections.models import Section
from django.db import models
from model_utils.managers import InheritanceManager


class Common(models.Model):
    title = models.CharField(max_length=20)
    sections = models.ManyToManyField(Section)
    slug = models.SlugField()

    objects = InheritanceManager()
    with_section = SectionSlugManager(section_field="sections")


class Article(Common):
    summary = models.TextField(default="Default", blank=True)


class Photo(Common):
    url = models.URLField(default="http://localhost/", blank=True)


class SimpleCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    slug = models.SlugField()

    objects = models.Manager()
    with_section = SectionSlugManager()


class SimpleArticle(SimpleCommon):
    summary = models.TextField(default="Default", blank=True)


class SimplePhoto(SimpleCommon):
    url = models.URLField(default="http://localhost/", blank=True)


class NonStandardField(models.Model):
    title = models.CharField(max_length=20)
    sections_by_another_name = models.ForeignKey(Section)
    slugs_by_another_name = models.SlugField()

    objects = models.Manager()
    with_section = SectionSlugManager(section_field="sections_by_another_name",
            slug_field="slugs_by_another_name")


class SectionForeignKeyCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    slug = models.SlugField()

    objects = InheritanceManager()
    with_section = SectionSlugManager()


class SectionForeignKeyArticle(SectionForeignKeyCommon):
    summary = models.TextField(default="Default", blank=True)    


class ComplexCommon(models.Model):
    title = models.CharField(max_length=20)
    primary_section = models.ForeignKey(Section)
    related_sections = models.ManyToManyField(Section, related_name='relatedcomplexcommon_set')
    slug = models.SlugField()

    objects = InheritanceManager()
    with_section = SectionSlugManager()

class ComplexArticle(ComplexCommon):
    summary = models.TextField(default="Default", blank=True)


class CustomSection(Section):
    pass
