from django.core.exceptions import ObjectDoesNotExist

from ._utils import *
from ..models import Section
from arm_sections_support.models import *

class SectionSlugManagerTestCase(ArmSectionsTestCase):
    """
    Test the workings of the SectionSlugManager.

    We compare using the `title` attribute because the QuerySet result
    and the self.object have some differences with attributes like
    `_primary_section_cache` and `simplecommon_ptr_id`.

    """
    def setUp(self):
        super(SectionSlugManagerTestCase, self).setUp()

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
        self.simple_article = SimpleArticle.objects.create(
                title="Test Simple Article",
                slug='test_simple_article',
                primary_section=self.sections[1]
            )
        self.simple_article2 = SimpleArticle.objects.create(
                title="Second Simple Article",
                slug='second_simple',
                primary_section=self.sections[2]
            )

    def test_get_by_slug_real(self):
        full_slug = "%s%s" % (self.sections[1].full_slug, self.simple_article.slug)
        self.assertEqual(SimpleArticle.with_section.get_by_slug(full_slug).title,
                         self.simple_article.title)

        full_slug = "%s%s" % (self.sections[2].full_slug, self.simple_article2.slug)
        self.assertEqual(SimpleArticle.with_section.get_by_slug(full_slug).title,
                         self.simple_article2.title)

        full_slug = "%s%s" % (self.sections[1].full_slug, self.article.slug)
        self.assertEqual(Article.with_section.get_by_slug(full_slug).title,
                         self.article.title)

        full_slug = "%s%s" % (self.sections[1].full_slug, self.article2.slug)
        self.assertEqual(Article.with_section.get_by_slug(full_slug).title,
                         self.article2.title)

    def test_get_by_slug_fake(self):
        full_slug = "%sfakearticle" % self.sections[1].full_slug
        with self.assertRaises(ObjectDoesNotExist):
            Article.with_section.get_by_slug(full_slug)
            SimpleArticle.with_section.get_by_slug(full_slug)

        full_slug = "fakesection/%s" % self.simple_article.slug
        with self.assertRaises(ObjectDoesNotExist):
            Article.with_section.get_by_slug(full_slug)
            SimpleArticle.with_section.get_by_slug(full_slug)

        full_slug = "fakesection/fakearticle"
        with self.assertRaises(ObjectDoesNotExist):
            Article.with_section.get_by_slug(full_slug)
            SimpleArticle.with_section.get_by_slug(full_slug)

    def test_get_by_slug_select_subclasses(self):
        # SimpleCommon does not use the InheritanceManager
        full_slug = "%s%s" % (self.sections[1].full_slug, self.simple_article.slug)
        self.assertNotEqual(type(SimpleCommon.with_section.get_by_slug(full_slug)),
                            type(self.simple_article))

        self.assertNotEqual(type(SimpleCommon.with_section.get_by_slug(full_slug)),
                            type(SimpleArticle.objects.get(pk=self.simple_article.pk)))

        self.assertEqual(type(SimpleCommon.with_section.get_by_slug(full_slug)),
                         type(SimpleCommon.objects.get(pk=self.simple_article.pk)))


        # Common has InheritanceManager
        full_slug = "%s%s" % (self.sections[1].full_slug, self.article.slug)
        self.assertEqual(type(Common.with_section.get_by_slug(full_slug)),
                         type(self.article))

        self.assertEqual(type(Common.with_section.get_by_slug(full_slug)),
                         type(Article.objects.get(pk=self.article.pk)))

    def test_get_by_slug_multiple(self):
        """
        There is no ordering on the Model or QuerySet,
        so we expect the first instance to be returned
        """
        dup_simple_article = SimpleArticle.objects.create(
                title="aaaa",
                slug='test_simple_article',
                primary_section=self.sections[1]
            )
        full_slug = "%s%s" % (self.sections[1].full_slug, self.simple_article.slug)
        self.assertEqual(SimpleArticle.with_section.get_by_slug(full_slug).title,
                         self.simple_article.title)

        dup_simple_article.delete()  # clean up

    def test_get_by_slug_malformed_slug(self):
        full_slug = "%s" % self.sections[1].full_slug
        with self.assertRaises(ObjectDoesNotExist):
            SimpleArticle.with_section.get_by_slug(full_slug)

        full_slug = "fakesection/"
        with self.assertRaises(ObjectDoesNotExist):
            SimpleArticle.with_section.get_by_slug(full_slug)

        full_slug = "fakesection"
        with self.assertRaises(ObjectDoesNotExist):
            SimpleArticle.with_section.get_by_slug(full_slug)
