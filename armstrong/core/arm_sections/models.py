from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


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
    summary = models.TextField()
    slug = models.SlugField()
    full_slug = models.CharField(max_length=255)

    parent = TreeForeignKey('self', null=True, blank=True)

    objects = SectionManager()

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
