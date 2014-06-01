from django.db import IntegrityError
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import FieldDoesNotExist

from armstrong.core.arm_sections.models import BaseSection, Section
from ._utils import ArmSectionsTestCase, override_settings
from .support.models import ComplexArticle, MultipleManyToManyModel


class ModelTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ModelTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')
        self.college = Section.objects.get(slug='college')

        self.complex_article = ComplexArticle.objects.create(
            title="Test Complex Article",
            slug='test_complex_article',
            primary_section=self.pro_sports)
        self.complex_article.related_sections = [self.weather]

        self.multiple_m2m_article = MultipleManyToManyModel.objects.create(
            title="Test Multple Many To Many Article",
            slug='test_multiple_m2m_article',
            primary_section=self.pro_sports)
        self.multiple_m2m_article.more_sections = [self.weather]

    def test_unicode_repr(self):
        self.assertEqual(u"%s" % self.weather, "Weather (weather/)")

    def test_subclass_must_define_parent_field_required_by_mptt(self):
        class NewSection(BaseSection):
            pass

        with self.assertRaises(FieldDoesNotExist):
            NewSection(title="one", slug="one")

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_item_related_name_returns_many_to_many_field_name(self):
        self.assertEqual(self.weather.item_related_name, 'related_sections')

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.SimpleCommon')
    def test_item_related_name_returns_none_without_many_to_many(self):
        self.assertEqual(self.weather.item_related_name, None)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_item_related_name_returns_none_with_multiple_many_to_many(self):
        self.assertEqual(self.weather.item_related_name, None)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_choose_field_name_returns_specified_field(self):
        self.assertEqual(
            self.weather._choose_field_name('related_sections'),
            'related_sections')

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_choose_field_name_errors_with_multiple_many_to_many(self):
        self.assertRaises(
            ImproperlyConfigured,
            self.weather._choose_field_name)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_ensure_section(self):
        self.assertNotIn(
            self.complex_article, self.college.items, msg='sanity check')
        self.college.add_item(self.complex_article)
        self.assertIn(self.complex_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_ensure_section_with_field_name(self):
        self.assertNotIn(
            self.multiple_m2m_article, self.college.items, msg='sanity check')
        self.college.add_item(
            self.multiple_m2m_article, field_name='more_sections')
        self.assertIn(self.multiple_m2m_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_remove_section(self):
        self.assertIn(
            self.complex_article, self.weather.items, msg='sanity check')
        self.weather.remove_item(self.complex_article)
        self.assertNotIn(self.complex_article, self.weather.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_remove_section_with_field_name(self):
        self.assertIn(
            self.multiple_m2m_article, self.weather.items, msg='sanity check')
        self.weather.remove_item(
            self.multiple_m2m_article, field_name='more_sections')
        self.assertNotIn(self.multiple_m2m_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_toggle_section_with_true_test_func(self):
        self.assertNotIn(
            self.complex_article, self.college.items, msg='sanity check')
        result = self.college.toggle_item(self.complex_article, lambda x: True)
        self.assertIn(self.complex_article, self.college.items)
        self.assertTrue(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_toggle_section_with_true_test_func_and_field_name(self):
        self.assertNotIn(
            self.multiple_m2m_article, self.college.items, msg='sanity check')
        result = self.college.toggle_item(
            self.multiple_m2m_article,
            lambda x: True,
            field_name='more_sections')
        self.assertIn(self.multiple_m2m_article, self.college.items)
        self.assertTrue(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_toggle_section_with_false_test_func(self):
        self.assertIn(
            self.complex_article, self.weather.items, msg='sanity check')
        result = self.weather.toggle_item(
            self.complex_article, lambda x: False)
        self.assertNotIn(self.complex_article, self.weather.items)
        self.assertFalse(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_toggle_section_with_false_test_func_and_field_name(self):
        self.assertIn(
            self.multiple_m2m_article, self.weather.items, msg='sanity check')
        result = self.weather.toggle_item(
            self.multiple_m2m_article,
            lambda x: False,
            field_name='more_sections')
        self.assertNotIn(self.multiple_m2m_article, self.weather.items)
        self.assertFalse(result)

    def test_insertion_order_of_new_root_section(self):
        new = Section.objects.create(
            title="A New Root",
            slug="zzz")
        roots = Section.tree.root_nodes()
        self.assertEqual(new, roots[0])

    def test_insertion_order_of_new_child_section(self):
        parent = Section.objects.get(slug="sports")
        new = Section.objects.create(
            title="A New Sport Subsection",
            slug="zzz",
            parent=parent)
        children = parent.get_children()
        self.assertEqual(new, children[0])

    def test_change_in_parent_slug_changes_child_full_slug(self):
        parent = Section.objects.get(slug="sports")
        child = Section.objects.get(slug="pro")
        self.assertEqual(child.full_slug, "sports/pro/")
        parent.slug = "new"
        parent.save()
        child = Section.objects.get(slug="pro")  # have to reload
        self.assertEqual(child.full_slug, "new/pro/")

    def test_no_change_in_parent_slug_does_not_change_child_full_slug(self):
        parent = Section.objects.get(slug="sports")
        child = Section.objects.get(slug="pro")
        self.assertEqual(child.full_slug, "sports/pro/")
        parent.slug = "sports"
        parent.save()
        child = Section.objects.get(slug="pro")  # have to reload
        self.assertEqual(child.full_slug, "sports/pro/")

    def test_duplicate_root_level_full_slug_raises_error(self):
        with self.assertRaises(IntegrityError):
            Section.objects.create(title="duplicate", slug="sports")

    def test_duplicate_nested_full_slug_raises_error(self):
        parent = Section.objects.get(slug="sports")
        with self.assertRaises(IntegrityError):
            Section.objects.create(
                title="duplicate", slug="pro", parent=parent)


class ManagerTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ManagerTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')
        self.college = Section.objects.get(slug='college')

        self.complex_article = ComplexArticle.objects.create(
            title="Test Complex Article",
            slug='test_complex_article',
            primary_section=self.pro_sports)
        self.complex_article.related_sections = [self.weather]

        self.multiple_m2m_article = MultipleManyToManyModel.objects.create(
            title="Test Multple Many To Many Article",
            slug='test_multiple_m2m_article',
            primary_section=self.pro_sports)
        self.multiple_m2m_article.more_sections = [self.weather]

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_ensure_section_id(self):
        self.assertNotIn(
            self.complex_article, self.college.items, msg='sanity check')
        Section.objects.add_item(self.complex_article, pk=self.college.pk)
        self.assertIn(self.complex_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_ensure_section_id_with_field_name(self):
        self.assertNotIn(
            self.multiple_m2m_article, self.college.items, msg='sanity check')
        Section.objects.add_item(
            self.multiple_m2m_article,
            field_name='more_sections',
            pk=self.college.pk)
        self.assertIn(self.multiple_m2m_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_remove_section_id(self):
        self.assertIn(
            self.complex_article, self.weather.items, msg='sanity check')
        Section.objects.remove_item(self.complex_article, pk=self.weather.pk)
        self.assertNotIn(self.complex_article, self.weather.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_remove_section_id_with_field_name(self):
        self.assertIn(
            self.multiple_m2m_article, self.weather.items, msg='sanity check')
        Section.objects.remove_item(
            self.multiple_m2m_article,
            field_name='more_sections',
            pk=self.weather.pk)
        self.assertNotIn(self.multiple_m2m_article, self.college.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_toggle_section_id_with_true_test_func(self):
        self.assertNotIn(
            self.complex_article, self.college.items, msg='sanity check')
        result = Section.objects.toggle_item(
            self.complex_article, lambda x: True, pk=self.college.pk)
        self.assertIn(self.complex_article, self.college.items)
        self.assertTrue(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_toggle_section_id_with_true_test_func_and_field_name(self):
        self.assertNotIn(
            self.multiple_m2m_article, self.college.items, msg='sanity check')
        result = Section.objects.toggle_item(
            self.multiple_m2m_article,
            lambda x: True,
            field_name='more_sections',
            pk=self.college.pk)
        self.assertIn(self.multiple_m2m_article, self.college.items)
        self.assertTrue(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.ComplexCommon')
    def test_can_toggle_section_id_with_false_test_func(self):
        self.assertIn(
            self.complex_article, self.weather.items, msg='sanity check')
        result = Section.objects.toggle_item(
            self.complex_article,
            lambda x: False,
            pk=self.weather.pk)
        self.assertNotIn(self.complex_article, self.weather.items)
        self.assertFalse(result)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='tests.support.models.MultipleManyToManyModel')
    def test_can_toggle_section_id_with_false_test_func_and_field_name(self):
        self.assertIn(
            self.multiple_m2m_article, self.weather.items, msg='sanity check')
        result = Section.objects.toggle_item(
            self.multiple_m2m_article,
            lambda x: False,
            field_name='more_sections', pk=self.weather.pk)
        self.assertNotIn(self.multiple_m2m_article, self.weather.items)
        self.assertFalse(result)
