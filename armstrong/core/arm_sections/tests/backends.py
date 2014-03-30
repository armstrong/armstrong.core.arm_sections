from datetime import datetime, timedelta
from model_utils.managers import InheritanceManager

from ._utils import ArmSectionsTestCase, override_settings
from ..models import Section
from arm_sections_support.models import *

from armstrong.core.arm_sections.backends import ItemFilter
from armstrong.core.arm_sections.managers import SectionSlugManager


class ManyToManyBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ManyToManyBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')
        self.pro_sports = Section.objects.get(slug='pro')

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

        self.subsection_article = Article.objects.create(
                title="Subsection Article",
                slug='subsection_article',
            )
        self.subsection_article.sections = [self.sports, self.pro_sports]

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common')
    def test_backend_with_articles_that_m2m_to_sections(self):
        self.assert_(self.article in self.sports.items)
        self.assert_(self.article2 in self.sports.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common')
    def test_article_in_section_and_subsection_appears_once_in_section(self):
        slug = self.subsection_article.slug
        in_sports = [a for a in self.sports.items if a.slug == slug]
        in_pro_sports = [a for a in self.pro_sports.items if a.slug == slug]
        self.assertEqual(len(in_sports), 1)
        self.assertEqual(len(in_pro_sports), 1)


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

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SectionForeignKeyCommon')
    def test_backend_with_foreign_key_articles(self):
        self.assert_(self.foreign_key_article in self.sports.items)
        self.assert_(self.foreign_key_article2 in self.weather.items)


class ComplexBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(ComplexBackendTestCase, self).setUp()

        self.pro_sports = Section.objects.get(slug='pro')
        self.sports = Section.objects.get(slug='sports')
        self.weather = Section.objects.get(slug='weather')

        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports
            )
        self.complex_article.related_sections = [self.weather, self.sports]

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon')
    def test_backend_with_m2m_and_foreign_key_articles(self):
        self.assert_(self.complex_article in self.pro_sports.items)
        self.assert_(self.complex_article in self.weather.items)

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon')
    def test_backend_no_duplicates_for_complex_articles(self):
        self.assertEqual(len(self.pro_sports.items), 1)
        self.assertEqual(len(self.weather.items), 1)


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

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon')
    def test_backend_with_parent_section_in_hierarchy(self):
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


class PublishedBackendTestCase(ArmSectionsTestCase):
    def setUp(self):
        super(PublishedBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')

        self.article = Article.objects.create(
                title="Test Article",
                slug='test_article',
                pub_date=datetime.now(),
                pub_status='P',
            )
        self.article.sections = [self.sports]
        self.article2 = Article.objects.create(
                title="Second Article",
                slug='second_article',
                pub_date=datetime.now(),
                pub_status='D',
            )
        self.article2.sections = [self.sports]
        self.article3 = Article.objects.create(
                title="Third Article",
                slug='third_article',
                pub_date=datetime.now() + timedelta(days=1),
                pub_status='P',
            )
        self.article3.sections = [self.sports]

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common')
    def test_published_doesnt_give_drafts(self):
        self.assertNotIn(self.article2, self.sports.published.all())

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common')
    def test_published_doesnt_give_future_articles(self):
        self.assertNotIn(self.article3, self.sports.published.all())

    @override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common')
    def test_published_gives_published_article(self):
        self.assertIn(self.article, self.sports.published.all())
