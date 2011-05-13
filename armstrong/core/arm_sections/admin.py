from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Section


class SectionAdmin(MPTTModelAdmin):
    exclude = ("full_slug", )

admin.site.register(Section, SectionAdmin)
