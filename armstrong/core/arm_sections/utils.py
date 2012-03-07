from django.conf import settings


def filter_item_rels(rels):
    model_rels = []
    for related in rels:
        found = "%s.%s" % (related.model.__module__,
                related.model.__name__)
        if found == settings.ARMSTRONG_SECTION_ITEM_MODEL:
            model_rels.append(related)
    return model_rels

def get_section_relations(Section):
    """Find every relationship between section and the item model."""
    all_rels = Section._meta.get_all_related_objects() + \
               Section._meta.get_all_related_many_to_many_objects()
    return filter_item_rels(all_rels)

def get_section_many_to_many_relations(Section):
	return filter_item_rels(Section._meta.get_all_related_many_to_many_objects())