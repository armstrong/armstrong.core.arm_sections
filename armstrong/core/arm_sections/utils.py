from django.conf import settings
from django.utils.importlib import import_module


def get_item_model_class():
    item_model_module_name, item_model_name = \
        settings.ARMSTRONG_SECTION_ITEM_MODEL.rsplit('.', 1)
    item_model_module = import_module(item_model_module_name)
    return getattr(item_model_module, item_model_name)

def filter_item_rels(rels):
    model_rels = []
    ItemModel = get_item_model_class()
    for related in rels:
        if issubclass(ItemModel, related.model):
            model_rels.append(related)
    return model_rels

def get_section_relations(Section):
    """Find every relationship between section and the item model."""
    all_rels = Section._meta.get_all_related_objects() + \
               Section._meta.get_all_related_many_to_many_objects()
    return filter_item_rels(all_rels)

def get_section_many_to_many_relations(Section):
    return filter_item_rels(Section._meta.get_all_related_many_to_many_objects())