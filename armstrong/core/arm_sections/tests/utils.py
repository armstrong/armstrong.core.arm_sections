from arm_sections_support.models import SimpleCommon

from ._utils import *

from .. import utils


class get_configured_item_modelTestCase(ArmSectionsTestCase):
    def test_returns_configured_model(self):
        m = "%s.FooBar" % self.__class__.__module__
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL=m):
            module, model = utils.get_module_and_model_names()
            self.assertEqual(self.__class__.__module__, module)
            self.assertEqual("FooBar", model)

    def test_provides_default_value(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL=False):
            module, model = utils.get_module_and_model_names()
            self.assertEqual("armstrong.apps.content.models", module)
            self.assertEqual("Content", model)


class get_item_model_classTestCase(ArmSectionsTestCase):
    def test_returns_specified_class(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SimpleCommon'):
            self.assertEqual(SimpleCommon, utils.get_item_model_class())