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
