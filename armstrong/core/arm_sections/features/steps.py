# -*- coding: utf-8 -*-
from copy import copy
from django.conf import settings
from django.db import connections
from django.db import DEFAULT_DB_ALIAS
from lettuce import *
from armstrong.core.arm_sections.models import Section


@before.each_scenario
def teardown_scenario(scenario):
    Section.objects.all().delete()
    world.created = []
    world.sections = []
    world.original_settings = copy(settings)


@after.each_scenario
def restore_settings(scenario):
    settings = world.original_settings
    [a.delete() for a in world.created]


@step(u'I have the following Sections:')
def given_i_have_the_following_sections(step):
    world.sections = []
    parent = False

    for row in step.hashes:
        data = copy(row)
        if 'parent__slug' in row:
            parent = data['parent__slug']
            del data['parent__slug']
            if parent == 'None':
                parent = None
        if parent:
            data["parent"] = Section.objects.get(slug=parent)
        world.sections.append(Section.objects.create(**data))
        

@step(u'I query for a section by slug "(.*)"')
def retrieve_by_slug(step, slug):
    # TODO: fix this
    world.section = Section.objects.get(full_slug=slug)


@step(u'I should have a Section with the following fields:')
def then_i_should_have_a_section_with_the_following_fields(step):
    for row in step.hashes:
        for key, value in row.items():
            if "__" in key:
                if value == "None":
                    value = None
                rel, key = key.split("__")
                related = getattr(world.section, rel, None)
                if value is None:
                    assert related is None
                else:
                    assert getattr(related, key) == value
            else:
                assert getattr(world.section, key) == value


@step(u'I start monitoring the number of queries run')
def start_monitoring_queries(step):
    # TODO: allow setting the db connection
    world.connection = connections[DEFAULT_DB_ALIAS]
    world.old_debug_cursor = world.connection.use_debug_cursor
    world.connection.use_debug_cursor = True
    world.starting_num_of_queries = len(world.connection.queries)


@step(u'I retrieve the children')
def retrieve_section_children(step):
    world.sections = world.section.get_descendants()


@step(u'I retrieve the section\'s parent')
def retrieve_section_parent(step):
    world.section = world.section.parent


@step(u'Then I should have the following sections:')
def then_i_should_have_the_following_sections(step):
    counter = 0

    for child in world.sections:
        row = step.hashes[counter]
        for key, value in row.items():
            if "__" in key:
                if value == "None":
                    value = None
                rel, key = key.split("__")
                related = getattr(child, rel, None)
                if value is None:
                    assert related is None, "child.%s is not Nones" % rel
                else:
                    assert getattr(related, key) == value
            else:
                assert getattr(child, key) == value, "(%s) child.%s == %s" % (child.title, key, value)
        counter += 1


@step(u'only (\d+) (query|queries) should have been run')
def and_only_1_query_should_have_been_run(step, num_queries, *args, **kwargs):
    num_queries = int(num_queries)
    end_queries = len(world.connection.queries)
    queries_run = end_queries - world.starting_num_of_queries
    world.connection.use_debug_cursor = world.old_debug_cursor
    assert queries_run == num_queries, "%s not equal to %s" % (queries_run,
            num_queries)


@step(u'I change the slug to "(.*)"')
def change_slug(step, new_slug):
    world.section.slug = new_slug
    world.section.save()


@step(u'I load all sections')
def load_all_sessions(step):
    world.sections = Section.objects.all()


@step(u'Given I have a "(.*)" model registered with the backends')
def setup_common_model(step, model):
    settings.ARMSTRONG_SECTION_ITEM_MODEL = "armstrong.core.arm_sections.tests.arm_sections_support.models.%s" % model


@step(u'I have the following models from support app:')
def and_i_have_the_following_models_from_support_app(step):
    from armstrong.core.arm_sections.tests.arm_sections_support import models
    for row in step.hashes:
        cls = getattr(models, row['model'])
        world.created.append(cls.objects.create(title=row['title'],
            section=world.section))


@step(u"I load the section's items")
def and_i_load_the_section_s_items(step):
    world.items = world.section.items


@step(u'Then I should have the following model:')
def then_i_should_have_the_following_model(step):
    assert len(world.items) == len(step.hashes)
    counter = 0
    for item in world.items:
        row = step.hashes[counter]
        assert row["model"] == item.__class__.__name__
        assert row["title"] == item.title
        counter += 1
