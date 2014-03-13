from django.db import models


class SectionSlugManager(models.Manager):
    def __init__(self, section_field="primary_section", slug_field="slug",
            *args, **kwargs):
        super(SectionSlugManager, self).__init__(*args, **kwargs)
        self.section_field = section_field
        self.slug_field = slug_field

    def get_by_slug(self, slug):
        if slug[-1] == "/":
            slug = slug[0:-1]
        if slug[0] == "/":
            slug = slug[1:]

        try:
            section_slug, content_slug = slug.rsplit("/", 1)
            section_slug += "/"
        except ValueError:
            raise self.model.DoesNotExist

        kwargs = {
                "%s__full_slug" % self.section_field: section_slug,
                self.slug_field: content_slug,
        }
        qs = self.model.objects.filter(**kwargs)
        if hasattr(qs, "select_subclasses"):
            qs = qs.select_subclasses()
        try:
            return qs[0]
        except IndexError:
            raise self.model.DoesNotExist
