from .items import ItemFilter


def find_related_models(section):
    return ItemFilter().run(section)
