from django.core.exceptions import ObjectDoesNotExist

from ._utils import *
from ..models import Section
from arm_sections_support.models import *

class SectionBackendTestCase(ArmSectionsTestCase):
    """
    """
    def setUp(self):
        super(SectionBackendTestCase, self).setUp()

        self.article = Article.objects.create(
                title="Test Article",
                slug='test_article',
            )
        self.article.sections = [self.sections[1]]
        self.article2 = Article.objects.create(
                title="Second Article",
                slug='second_article',
            )
        self.article2.sections = [self.sections[1]]
        self.foreign_key_article = SectionForeignKeyArticle.objects.create(
                title="Test Foreign Key Article",
                slug='test_foreign_key_article',
                primary_section=self.sections[1]
            )
        self.foreign_key_article2 = SectionForeignKeyArticle.objects.create(
                title="Second Foreign Key Article",
                slug='second_foreign_key',
                primary_section=self.sections[2]
            )
        self.complex_article = ComplexArticle.objects.create(
                title="Test Complex Article",
                slug='test_complex_article',
                primary_section=self.sections[1]
            )
        self.complex_article.related_sections = [self.sections[2]]

    def test_backend_with_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.Common'):
            self.assert_(self.article in self.sections[1].items)
            self.assert_(self.article2 in self.sections[1].items)

    def test_backend_with_foreign_key_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.SectionForeignKeyCommon'):
            self.assert_(self.foreign_key_article in self.sections[1].items)
            self.assert_(self.foreign_key_article2 in self.sections[2].items)

    def test_backend_with_complex_articles(self):
        with override_settings(ARMSTRONG_SECTION_ITEM_MODEL='armstrong.core.arm_sections.tests.arm_sections_support.models.ComplexCommon'):
            self.assert_(self.complex_article in self.sections[1].items)
            self.assert_(self.complex_article in self.sections[2].items)
