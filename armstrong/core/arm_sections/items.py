from django.conf import settings
from django.db.models import Q


class ItemFilter(object):
    def get_section_relations(self, section):
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
        kwargs_list = [{rel.field.name: section} for rel in rels]
        q = Q(**kwargs_list[0])
        for kwargs in kwargs_list[1:]:
            q |= Q(**kwargs)
        return rels[0].model.objects.filter(q)

    def process_items(self, items):
        if hasattr(items, 'select_subclasses'):
            items = items.select_subclasses()
        return items

    def run(self, section):
        relations = self.get_section_relations(section)
        items = self.filter_objects_by_section(relations, section)
        return self.process_items(items)
