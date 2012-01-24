from django.conf import settings
from django.db.models import Q


class ItemFilter(object):
    manager_attr = '_default_manager'

    def get_manager(self, model):
        """Return the desired manager for the item model."""
        return getattr(model, self.manager_attr)

    def get_section_relations(self, section):
        """Find every relationship between section and the item model."""
        all_rels = section._meta.get_all_related_objects() + \
                   section._meta.get_all_related_many_to_many_objects()
        model_rels = []
        for related in all_rels:
            found = "%s.%s" % (related.model.__module__,
                    related.model.__name__)
            if found == settings.ARMSTRONG_SECTION_ITEM_MODEL:
                model_rels.append(related)
        return model_rels

    def filter_objects_by_section(self, rels, section):
        """Build a queryset containing all objects in the section subtree."""
        subtree = section.get_descendants(include_self=True)
        kwargs_list = [{'%s__in' % rel.field.name: subtree} for rel in rels]
        q = Q(**kwargs_list[0])
        for kwargs in kwargs_list[1:]:
            q |= Q(**kwargs)
        return self.get_manager(rels[0].model).filter(q)

    def process_items(self, items):
        """
        Perform extra actions on the filtered items.

        Example: Further filtering the items in the section to meet a
        custom need.
        """
        if hasattr(items, 'select_subclasses'):
            items = items.select_subclasses()
        return items

    def __call__(self, section):
        relations = self.get_section_relations(section)
        items = self.filter_objects_by_section(relations, section)
        return self.process_items(items)


find_related_models = ItemFilter()
