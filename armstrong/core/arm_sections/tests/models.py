from django.core.exceptions import ImproperlyConfigured
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

        self.multiple_many_to_many_article = MultipleManyToManyModel.objects.create(
                title="Test Multple Many To Many Article",
                slug='test_multiple_many_to_many_article',
                primary_section=self.pro_sports,
            )
        self.multiple_many_to_many_article.more_sections = [self.weather]

    def test_item_related_name_returns_many_to_many_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertEqual(self.weather.item_related_name, 'related_sections')

    def test_item_related_name_returns_none_without_many_to_many(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SimpleCommon'):
            self.assertEqual(self.weather.item_related_name, None)

    def test_item_related_name_returns_none_with_multiple_many_to_many(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertEqual(self.weather.item_related_name, None)

    def test_choose_field_name_returns_specified_field(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertEqual(self.weather._choose_field_name('related_sections'), 'related_sections')

    def test_choose_field_name_errors_with_multiple_many_to_many(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertRaises(ImproperlyConfigured, self.weather._choose_field_name)

    def test_can_ensure_section(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertNotIn(self.complex_article, self.college.items, msg='sanity check')
            self.college.add_item(self.complex_article)
            self.assertIn(self.complex_article, self.college.items)

    def test_can_ensure_section_with_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items, msg='sanity check')
            self.college.add_item(self.multiple_many_to_many_article, field_name='more_sections')
            self.assertIn(self.multiple_many_to_many_article, self.college.items)

    def test_can_remove_section(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertIn(self.complex_article, self.weather.items, msg='sanity check')
            self.weather.remove_item(self.complex_article)
            self.assertNotIn(self.complex_article, self.weather.items)

    def test_can_remove_section_with_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertIn(self.multiple_many_to_many_article, self.weather.items, msg='sanity check')
            self.weather.remove_item(self.multiple_many_to_many_article, field_name='more_sections')
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items)

    def test_can_toggle_section_with_true_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertNotIn(self.complex_article, self.college.items, msg='sanity check')
            result = self.college.toggle_item(self.complex_article, lambda x: True)
            self.assertIn(self.complex_article, self.college.items)
            self.assertTrue(result)

    def test_can_toggle_section_with_true_test_func_and_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items, msg='sanity check')
            result = self.college.toggle_item(self.multiple_many_to_many_article, lambda x: True, field_name='more_sections')
            self.assertIn(self.multiple_many_to_many_article, self.college.items)
            self.assertTrue(result)

    def test_can_toggle_section_with_false_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertIn(self.complex_article, self.weather.items, msg='sanity check')
            result = self.weather.toggle_item(self.complex_article, lambda x: False)
            self.assertNotIn(self.complex_article, self.weather.items)
            self.assertFalse(result)

    def test_can_toggle_section_with_false_test_func_and_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertIn(self.multiple_many_to_many_article, self.weather.items, msg='sanity check')
            result = self.weather.toggle_item(self.multiple_many_to_many_article, lambda x: False, field_name='more_sections')
            self.assertNotIn(self.multiple_many_to_many_article, self.weather.items)
            self.assertFalse(result)


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

        self.multiple_many_to_many_article = MultipleManyToManyModel.objects.create(
                title="Test Multple Many To Many Article",
                slug='test_multiple_many_to_many_article',
                primary_section=self.pro_sports,
            )
        self.multiple_many_to_many_article.more_sections = [self.weather]

    def test_can_ensure_section_id(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertNotIn(self.complex_article, self.college.items, msg='sanity check')
            Section.objects.add_item(self.complex_article, pk=self.college.pk)
            self.assertIn(self.complex_article, self.college.items)

    def test_can_ensure_section_id_with_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items, msg='sanity check')
            Section.objects.add_item(self.multiple_many_to_many_article, field_name='more_sections', pk=self.college.pk)
            self.assertIn(self.multiple_many_to_many_article, self.college.items)

    def test_can_remove_section_id(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertIn(self.complex_article, self.weather.items, msg='sanity check')
            Section.objects.remove_item(self.complex_article, pk=self.weather.pk)
            self.assertNotIn(self.complex_article, self.weather.items)

    def test_can_remove_section_id_with_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertIn(self.multiple_many_to_many_article, self.weather.items, msg='sanity check')
            Section.objects.remove_item(self.multiple_many_to_many_article, field_name='more_sections', pk=self.weather.pk)
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items)

    def test_can_toggle_section_id_with_true_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertNotIn(self.complex_article, self.college.items, msg='sanity check')
            result = Section.objects.toggle_item(self.complex_article, lambda x: True, pk=self.college.pk)
            self.assertIn(self.complex_article, self.college.items)
            self.assertTrue(result)

    def test_can_toggle_section_id_with_true_test_func_and_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertNotIn(self.multiple_many_to_many_article, self.college.items, msg='sanity check')
            result = Section.objects.toggle_item(self.multiple_many_to_many_article, lambda x: True, field_name='more_sections', pk=self.college.pk)
            self.assertIn(self.multiple_many_to_many_article, self.college.items)
            self.assertTrue(result)

    def test_can_toggle_section_id_with_false_test_func(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assertIn(self.complex_article, self.weather.items, msg='sanity check')
            result = Section.objects.toggle_item(self.complex_article, lambda x: False, pk=self.weather.pk)
            self.assertNotIn(self.complex_article, self.weather.items)
            self.assertFalse(result)

    def test_can_toggle_section_id_with_false_test_func_and_field_name(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.MultipleManyToManyModel'):
            self.assertIn(self.multiple_many_to_many_article, self.weather.items, msg='sanity check')
            result = Section.objects.toggle_item(self.multiple_many_to_many_article, lambda x: False, field_name='more_sections', pk=self.weather.pk)
            self.assertNotIn(self.multiple_many_to_many_article, self.weather.items)
            self.assertFalse(result)