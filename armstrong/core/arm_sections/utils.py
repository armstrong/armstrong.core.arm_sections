from django.conf import settings
from django.utils.importlib import import_module


def get_module_and_model_names():
    s = (getattr(settings, "ARMSTRONG_SECTION_ITEM_MODEL", False) or
            "armstrong.apps.content.models.Content")
    return s.rsplit(".", 1)


def get_item_model_class():
    module_name, class_name = get_module_and_model_names()
    module = import_module(module_name)
    return getattr(module, class_name)

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
