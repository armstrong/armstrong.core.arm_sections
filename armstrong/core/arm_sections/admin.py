from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Section


class SectionAdmin(MPTTModelAdmin):
    exclude = ("full_slug", )
    search_fields = ('title', 'summary')


admin.site.register(Section, SectionAdmin)


# DEPRECATED: To be removed in ArmSections 2.0
# (This also should have been in a `forms.py` file and renamed to
# `SectionTreeFormMixin` as it's not limited to Admin Forms.)
import warnings
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
from mptt.models import MPTTModel


class SectionTreeAdminMixin(object):  # pragma: no cover
    """Form mixin for the tree display of Section <select>s"""

    def __init__(self, *args, **kwargs):
        msg = ("SectionTreeAdminMixin is deprecated and will be removed in "
               "ArmSections 2.0. Explicitly use mptt's TreeForeignKey/"
               "TreeOneToOneField/TreeManyToManyField in your model "
               "definitions.")
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        super(SectionTreeAdminMixin, self).__init__(*args, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if issubclass(db_field.rel.to, MPTTModel):
            required = db_field.formfield().required
            return TreeNodeChoiceField(
                queryset=db_field.rel.to.objects.all(),
                required=required)
        return super(SectionTreeAdminMixin, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if issubclass(db_field.rel.to, MPTTModel):
            required = db_field.formfield().required
            return TreeNodeMultipleChoiceField(
                queryset=db_field.rel.to.objects.all(),
                required=required)
        return super(SectionTreeAdminMixin, self)\
            .formfield_for_manytomany(db_field, request, **kwargs)
