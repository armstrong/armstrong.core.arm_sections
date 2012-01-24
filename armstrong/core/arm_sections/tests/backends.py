from django.core.exceptions import ObjectDoesNotExist

from ._utils import *
from ..models import Section
from arm_sections_support.models import *

class SectionBackendTestCase(ArmSectionsTestCase):
    """
    """
    def setUp(self):
        super(SectionBackendTestCase, self).setUp()

        self.sports = Section.objects.get(slug='sports')
        self.pro_sports = Section.objects.get(slug='pro')
        self.weather = Section.objects.get(slug='weather')

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
        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.pro_sports
            )
        self.complex_article.related_sections = [self.weather]

    def test_backend_with_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common'):
            self.assert_(self.article in self.sports.items)
            self.assert_(self.article2 in self.sports.items)

    def test_backend_with_foreign_key_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SectionForeignKeyCommon'):
            self.assert_(self.foreign_key_article in self.sports.items)
            self.assert_(self.foreign_key_article2 in self.weather.items)

    def test_backend_with_complex_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.pro_sports.items)
            self.assert_(self.complex_article in self.weather.items)

    def test_backend_with_section_hierarchy(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.sports.items)
            self.assert_(self.complex_article in self.pro_sports.items)
