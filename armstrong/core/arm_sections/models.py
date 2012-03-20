from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from armstrong.utils.backends import GenericBackend

from .utils import get_section_many_to_many_relations

__BACKEND_MODULE = "armstrong.core.arm_sections.backends.%s"
SECTION_ITEM_BACKEND = (GenericBackend('ARMSTRONG_SECTION_ITEM_BACKEND',
        defaults=__BACKEND_MODULE % "ItemFilter")
    .get_backend())
SECTION_PUBLISHED_BACKEND = (GenericBackend(
        'ARMSTRONG_SECTION_PUBLISHED_BACKEND',
        defaults=__BACKEND_MODULE % "PublishedItemFilter")
    .get_backend())


class SectionManager(models.Manager):
    def get(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        if 'full_slug' in defaults:
            if defaults['full_slug'] and defaults['full_slug'][-1] != "/":
                defaults['full_slug'] += "/"
        return super(SectionManager, self).get(**defaults)

    def add_item(self, item, field_name=None, **kwargs):
        section = self.get_query_set().get(**kwargs)
        section.add_item(item, field_name=field_name)

    def remove_item(self, item, field_name=None, **kwargs):
        section = self.get_query_set().get(**kwargs)
        section.remove_item(item, field_name=field_name)

    def toggle_item(self, item, test_func, field_name=None, **kwargs):
        section = self.get_query_set().get(**kwargs)
        return section.toggle_item(item, test_func, field_name=field_name)


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

    @property
    def published(self):
        return SECTION_PUBLISHED_BACKEND(self)

    @property
    def item_related_name(self):
        """
        The ManyToMany field on the item class pointing to this class.

        If there is more than one field, this value will be None.
        """
        if not hasattr(self, '_item_related_name'):
            many_to_many_rels = \
                get_section_many_to_many_relations(self.__class__)
            if len(many_to_many_rels) != 1:
                self._item_related_name = None
            else:
                self._item_related_name = many_to_many_rels[0].field.name
        return self._item_related_name

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

    def _choose_field_name(self, specified_field=None):
        if specified_field is not None:
            return specified_field
        if self.item_related_name is None:
            raise ImproperlyConfigured(
                "A field_name must be specified if there isn't a single "
                "section ManyToMany relation.")
        return self.item_related_name

    def add_item(self, item, field_name=None):
        """
        Add the item to the specified section.

        Intended for use with items of settings.ARMSTRONG_SECTION_ITEM_MODEL.
        Behavior on other items is undefined.
        """
        field_name = self._choose_field_name(field_name)
        related_manager = getattr(item, field_name)
        related_manager.add(self)

    def remove_item(self, item, field_name=None):
        """
        Remove the item from the specified section.

        Intended for use with items of settings.ARMSTRONG_SECTION_ITEM_MODEL.
        Behavior on other items is undefined.
        """
        field_name = self._choose_field_name(field_name)
        related_manager = getattr(item, field_name)
        related_manager.remove(self)

    def toggle_item(self, item, test_func, field_name=None):
        """
        Toggles the section based on test_func.

        test_func takes an item and returns a boolean. If it returns True, the
        item will be added to the given section. It will be removed from the
        section otherwise.

        Intended for use with items of settings.ARMSTRONG_SECTION_ITEM_MODEL.
        Behavior on other items is undefined.
        """
        if test_func(item):
            self.add_item(item, field_name)
            return True
        else:
            self.remove_item(item, field_name)
            return False
