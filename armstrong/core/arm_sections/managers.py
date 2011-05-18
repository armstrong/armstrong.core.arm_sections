from django.db import models


class SectionSlugManager(models.Manager):
    def get_by_slug(self, slug):
        section_slug, content_slug = slug.rsplit("/", 1)
        section_slug += "/"
        return self.model.objects.filter(primary_section__full_slug=section_slug,
                slug=content_slug).select_subclasses()[0]
