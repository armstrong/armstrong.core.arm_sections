from django.utils.unittest import skip

from ..models import Section

from ._utils import *
from arm_sections_support.models import *


class ModelTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ModelTestCase, self).setUp()

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
            self.college.add_item(self.complex_article)
            self.assert_(self.complex_article in self.college.items)

    def test_can_remove_section(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            self.weather.remove_item(self.complex_article)
            self.assert_(self.complex_article not in self.weather.items)

    def test_can_set_section_with_true_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article not in self.college.items)
            self.college.set_item(self.complex_article, lambda x: True)
            self.assert_(self.complex_article in self.college.items)

    def test_can_set_section_with_false_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            self.weather.set_item(self.complex_article, lambda x: False)
            self.assert_(self.complex_article not in self.weather.items)


class ManagerTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ManagerTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')
        self.college = Section.objects.get(slug='college')

        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports,
            )
        self.complex_article.related_sections = [self.weather]

    def test_can_ensure_section_id(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article not in self.college.items)
            Section.objects.add_item(self.college.pk, self.complex_article)
            self.assert_(self.complex_article in self.college.items)

    def test_can_remove_section_id(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            Section.objects.remove_item(self.weather.pk, self.complex_article)
            self.assert_(self.complex_article not in self.weather.items)

    def test_can_set_section_id_with_true_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article not in self.college.items)
            Section.objects.set_item(self.college.pk, self.complex_article, lambda x: True)
            self.assert_(self.complex_article in self.college.items)

    def test_can_set_section_id_with_false_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.weather.items)
            Section.objects.set_item(self.weather.pk, self.complex_article, lambda x: False)
            self.assert_(self.complex_article not in self.weather.items)