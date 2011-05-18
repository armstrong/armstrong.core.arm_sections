from django.db import models


class SectionSlugManager(models.Manager):
    def get_by_slug(self, slug):
        section_slug, content_slug = slug.rsplit("/", 1)
        section_slug += "/"
        qs = self.model.objects.filter(primary_section__full_slug=section_slug,
                slug=content_slug)
        if hasattr(qs, "select_subclasses"):
            qs = qs.select_subclasses()
        try:
            return qs[0]
        except IndexError:
            raise self.model.DoesNotExist
