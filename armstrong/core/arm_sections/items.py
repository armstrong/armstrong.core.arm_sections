from django.core.exceptions import ImproperlyConfigured

from .utils import get_section_many_to_many_relations


def _get_section_field_name_for_items(section):
    many_to_many_rels = \
        get_section_many_to_many_relations(section.__class__)
    if len(many_to_many_rels) != 1:
        print len(many_to_many_rels)
        raise ImproperlyConfigured(
            "A field_name must be specified if there isn't a single "
            "section ManyToMany relation.")
    return many_to_many_rels[0].field.name

def ensure_item_in_section_func(section, field_name=None):
    '''Generates a function that ensures an item is in the specified section.

    The returned function is intended for use with items of
    settings.ARMSTRONG_SECTION_ITEM_MODEL. Behavior on other items is
    undefined.
    '''
    # If no field name was given, use the ManyToManyField on the item class
    # if only one is present.
    if field_name is None:
        field_name = _get_section_field_name_for_items(section)

    def ensure_item_in_section(item):
        related_manager = getattr(item, field_name)
        related_manager.add(section)

    return ensure_item_in_section


def remove_item_from_section_func(section, field_name=None):
    '''Generates a function that removes an item from the specified section.

    The returned function is intended for use with items of
    settings.ARMSTRONG_SECTION_ITEM_MODEL. Behavior on other items is
    undefined.
    '''
    # If no field name was given, use the ManyToManyField on the item class
    # if only one is present.
    if field_name is None:
        field_name = _get_section_field_name_for_items(section)

    def remove_item_from_section(item):
        related_manager = getattr(item, field_name)
        related_manager.remove(section)

    return remove_item_from_section


def set_item_section_func(section, test_func, field_name=None):
    '''Generates a function that toggles the section based on test_func.

    test_func takes an item and returns a boolean. If it returns True, the
    item will be added to the given section. It will be removed from the
    section otherwise.

    The returned function is intended for use with items of
    settings.ARMSTRONG_SECTION_ITEM_MODEL. Behavior on other items is
    undefined.
    '''
    ensure_item_in_section = ensure_item_in_section_func(section,
        field_name=field_name)
    remove_item_from_section = remove_item_from_section_func(section,
        field_name=field_name)

    def set_item_section(item):
        if test_func(item):
            ensure_item_in_section(item)
            return True
        else:
            remove_item_from_section(item)
            return False

    return set_item_section