from django.conf import settings


class ItemFilter(object):
    def get_section_relation(self, section):
        rel = None
        relateds = section._meta.get_all_related_objects() + \
                   section._meta.get_all_related_many_to_many_objects()
        for related in relateds:
            found = "%s.%s" % (related.model.__module__,
                    related.model.__name__)
            if found == settings.ARMSTRONG_SECTION_ITEM_MODEL:
                return related

    def filter_objects_by_section(self, rel, section):
        kwargs = {rel.field.name: section}
        return rel.model.objects.filter(**kwargs)

    def process_items(self, items):
        if hasattr(items, 'select_subclasses'):
            items = items.select_subclasses()
        return items

    def run(self, section):
        relation = self.get_section_relation(section)
        items = self.filter_objects_by_section(relation, section)
        return self.process_items(items)
