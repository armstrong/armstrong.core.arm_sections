from armstrong.core.arm_sections import utils
from armstrong.core.arm_sections.models import Section

from ._utils import ArmSectionsTestCase, override_settings
from .support.models import SimpleCommon


def rel_field_names(rels):
    return [rel.field.name for rel in rels]


class get_configured_item_modelTestCase(ArmSectionsTestCase):
    def test_returns_configured_model(self):
        m = "%s.FooBar" % self.__class__.__module__
        with self.settings(ARMSTRONG_SECTION_ITEM_MODEL=m):
            module, model = utils.get_module_and_model_names()
            self.assertEqual(self.__class__.__module__, module)
            self.assertEqual("FooBar", model)

    def test_provides_default_value(self):
        with self.settings(ARMSTRONG_SECTION_ITEM_MODEL=False):
            module, model = utils.get_module_and_model_names()
            self.assertEqual("armstrong.apps.content.models", module)
            self.assertEqual("Content", model)


class get_item_model_classTestCase(ArmSectionsTestCase):

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.SimpleCommon')
    def test_returns_specified_class(self):
        self.assertEqual(SimpleCommon, utils.get_item_model_class())


class get_section_relationsTestCase(ArmSectionsTestCase):
    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.SimpleCommon')
    def test_returns_relation_for_foreign_key_only(self):
        self.assertEqual(
            ['primary_section'],
            rel_field_names(utils.get_section_relations(Section)))

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_returns_relations_for_foreign_key_and_many_to_many(self):
        self.assertEqual(
            ['primary_section', 'related_sections'],
            rel_field_names(utils.get_section_relations(Section)))

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_returns_relations_for_subclass_with_foreign_key_and_m2m(self):
        self.assertEqual(
            ['primary_section', 'related_sections', 'more_sections'],
            rel_field_names(utils.get_section_relations(Section)))


class get_section_many_to_many_relationsTestCase(ArmSectionsTestCase):
    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.SimpleCommon')
    def test_returns_no_relations_for_foreign_key_only(self):
        self.assertEqual(
            [],
            rel_field_names(utils.get_section_many_to_many_relations(Section)))

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_returns_relation_for_foreign_key_and_many_to_many(self):
        self.assertEqual(
            ['related_sections'],
            rel_field_names(utils.get_section_many_to_many_relations(Section)))

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_returns_relations_for_subclass_with_foreign_key_and_m2m(self):
        self.assertEqual(
            ['related_sections', 'more_sections'],
            rel_field_names(utils.get_section_many_to_many_relations(Section)))
