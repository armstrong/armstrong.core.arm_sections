from ..models import Section
from ..items import (ensure_item_in_section_func, remove_item_from_section_func,
    set_item_section_func)

from ._utils import *
from arm_sections_support.models import *


class ItemsTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ItemsTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')
        self.college = Section.objects.get(slug='college')

        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports,
            )
        self.complex_article.related_sections = [self.weather]

    def test_can_ensure_section(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article not in self.college.items)
            ensure_func = ensure_item_in_section_func(self.college)
            ensure_func(self.complex_article)
            self.assert_(self.complex_article in self.college.items)

    def test_can_remove_section(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            remove_func = remove_item_from_section_func(self.weather)
            remove_func(self.complex_article)
            self.assert_(self.complex_article not in self.college.items)

    def test_can_set_section_with_true_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article not in self.college.items)
            set_func = set_item_section_func(self.college, lambda x: True)
            set_func(self.complex_article)
            self.assert_(self.complex_article in self.college.items)

    def test_can_set_section_with_false_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            set_func = set_item_section_func(self.weather, lambda x: False)
            set_func(self.complex_article)
            self.assert_(self.complex_article not in self.weather.items)