from django.core.exceptions import ObjectDoesNotExist

from ._utils import *
from ..models import Section
from arm_sections_support.models import *

from armstrong.core.arm_sections.backends import ItemFilter
from armstrong.core.arm_sections.managers import SectionSlugManager
from model_utils.managers import InheritanceManager


class ManyToManyBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ManyToManyBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')

        self.article = Article.objects.create(
                title="Test Article",
                slug='test_article',
            )
        self.article.sections = [self.sports]
        self.article2 = Article.objects.create(
                title="Second Article",
                slug='second_article',
            )
        self.article2.sections = [self.sports]

    def test_backend_with_articles(self):
        """
        Test fetching items for content with a many-to-many relationship to sections.
        """
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common'):
            self.assert_(self.article in self.sports.items)
            self.assert_(self.article2 in self.sports.items)


class ForeignKeyBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ForeignKeyBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')
        self.weather = Section.objects.get(slug='weather')

        self.foreign_key_article = SectionForeignKeyArticle.objects.create(
                title="Test Foreign Key Article",
                slug='test_foreign_key_article',
                primary_section=self.sports
            )
        self.foreign_key_article2 = SectionForeignKeyArticle.objects.create(
                title="Second Foreign Key Article",
                slug='second_foreign_key',
                primary_section=self.weather
            )

    def test_backend_with_foreign_key_articles(self):
        """
        Test fetching items for content with a foreign key relationship to sections.
        """
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SectionForeignKeyCommon'):
            self.assert_(self.foreign_key_article in self.sports.items)
            self.assert_(self.foreign_key_article2 in self.weather.items)


class ComplexBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ComplexBackendTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')

        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports
            )
        self.complex_article.related_sections = [self.weather]

    def test_backend_with_complex_articles(self):
        """
        Test fetching items for content with foreign key and many-to-many relationships to sections.
        """
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.pro_sports.items)
            self.assert_(self.complex_article in self.weather.items)

class HierarchyBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(HierarchyBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')
        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')

        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports
            )
        self.complex_article.related_sections = [self.weather]

    def test_backend_with_section_hierarchy(self):
        """
        Test fetching items for a parent section of the associated section.
        """
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.sports.items)
            self.assert_(self.complex_article in self.pro_sports.items)

class ManagerTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ManagerTestCase, self).setUp()
        self.item_filter = ItemFilter()

    def test_default_manager(self):
        """
        Test ItemFilter.get_manager with the default manager.
        """
        self.assertIsA(self.item_filter.get_manager(ComplexCommon),
            InheritanceManager)

    def test_custom_manager(self):
        """
        Test ItemFilter.get_manager with a custom manager.
        """
        self.item_filter.manager_attr = 'with_section'
        self.assertIsA(self.item_filter.get_manager(ComplexCommon),
            SectionSlugManager)
