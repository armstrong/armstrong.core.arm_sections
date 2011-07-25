from django.conf import settings
from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from armstrong.utils.backends import GenericBackend

SECTION_ITEM_BACKEND = GenericBackend('ARMSTRONG_SECTION_ITEM_BACKEND',
        defaults="armstrong.core.arm_sections.backends.find_related_models")\
                .get_backend


class SectionManager(models.Manager):
    def get(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        if 'full_slug' in defaults:
            if defaults['full_slug'] and defaults['full_slug'][-1] != "/":
                defaults['full_slug'] += "/"
        return super(SectionManager, self).get(**defaults)


class Section(MPTTModel):
    title = models.CharField(max_length=255)
    summary = models.TextField(default="", blank=True)
    slug = models.SlugField()
    full_slug = models.CharField(max_length=255, blank=True)

    parent = TreeForeignKey('self', null=True, blank=True)

    objects = SectionManager()

    @property
    def items(self):
        return SECTION_ITEM_BACKEND(self)

    def save(self, *args, **kwargs):
        orig_full_slug = self.full_slug
        if self.parent:
            self.full_slug = "%s%s/" % (self.parent.full_slug, self.slug)
        else:
            self.full_slug = "%s/" % self.slug
        obj = super(Section, self).save(*args, **kwargs)
        if orig_full_slug != self.full_slug:
            for child in self.get_children():
                child.save()
        return obj

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.full_slug)
