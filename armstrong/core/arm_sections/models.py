from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class Section(MPTTModel):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    slug = models.SlugField()

    parent = TreeForeignKey('self', null=True, blank=True)
