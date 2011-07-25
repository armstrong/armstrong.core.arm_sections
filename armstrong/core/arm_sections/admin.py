from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField
from mptt.forms import TreeNodeMultipleChoiceField
from mptt.models import MPTTModel

from .models import Section

EMPTY_LABEL = u"---------"


class SectionTreeAdminMixin(object):
    """
    Provides a mixin for dealing with tree display of Section <select>s in
    admin forms
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if issubclass(db_field.rel.to, MPTTModel):
            required = db_field.formfield().required
            return TreeNodeChoiceField(queryset=db_field.rel.to.objects.all(),
                    required=required, empty_label=EMPTY_LABEL)
        return super(SectionTreeAdminMixin, self)\
                .formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if issubclass(db_field.rel.to, MPTTModel):
            required = db_field.formfield().required
            return TreeNodeMultipleChoiceField(empty_label=EMPTY_LABEL,
                    queryset=db_field.rel.to.objects.all(), required=required)
        return super(SectionTreeAdminMixin, self)\
                .formfield_for_manytomany(db_field, request, **kwargs)


class SectionAdmin(MPTTModelAdmin):
    exclude = ("full_slug", )


admin.site.register(Section, SectionAdmin)
