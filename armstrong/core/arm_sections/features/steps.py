# -*- coding: utf-8 -*-
from lettuce import step, world
from armstrong.core.arm_sections.models import Section


@step(u'Given I have the following Sections:')
def given_i_have_the_following_sections(step):
    world.sections = []

    for row in step.hashes:
        if 'parent__slug' in row:
            parent = row['parent__slug']
            if parent == 'None':
                parent = None
        world.sections.append(Section.objects.create(**row))
        


@step(u'Given that I have a model')
def given_that_i_have_a_model(step):
    assert False, 'This step must be implemented'


@step(u'And that model has a')
def and_that_model_has_a(step):
    assert False, 'This step must be implemented'


@step(u'Given I have a section called "(.*)"')
def given_i_have_a_section_called_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And I have 2 "(.*)" models')
def and_i_have_2_group1_models(step, group1):
    assert False, 'This step must be implemented'


@step(u'And those models are configured to go into the "(.*)" section')
def those_models_are_configured_to_go_into_the_group1_section(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I retrieve a Section with the name "(.*)"')
def when_i_retrieve_a_section_with_the_name_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And ask for all its "(.*)"')
def and_ask_for_all_its_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'Then I should see the two models created earlier')
def then_i_should_see_the_two_models_created_earlier(step):
    assert False, 'This step must be implemented'


@step(u'And I have 1 "(.*)" model')
def and_i_have_1_group1_model(step, group1):
    assert False, 'This step must be implemented'



@step(u'When I query for a Section by slug "(.*)"')
def when_i_query_for_a_section_by_slug_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'Then I should have a Section with the following fields:')
def then_i_should_have_a_section_with_the_following_fields(step):
    assert False, 'This step must be implemented'


@step(u'When I query for a section by slug "(.*)"')
def when_i_query_for_a_section_by_slug_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And I query for a section by slug "(.*)"')
def and_i_query_for_a_section_by_slug_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I retrieve the section\'s parent')
def when_i_retrieve_the_section_s_parent(step):
    assert False, 'This step must be implemented'


@step(u'And I have the Section with the slug "(.*)"')
def and_i_have_the_section_with_the_slug_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I start monitoring the number of queries run')
def when_i_start_monitoring_the_number_of_queries_run(step):
    assert False, 'This step must be implemented'


@step(u'And I retrieve the children')
def and_i_retrieve_the_children(step):
    assert False, 'This step must be implemented'


@step(u'Then I should have the following sections:')
def then_i_should_have_the_following_sections(step):
    assert False, 'This step must be implemented'


@step(u'And only 1 query should have been run')
def and_only_1_query_should_have_been_run(step):
    assert False, 'This step must be implemented'


@step(u'Given I have the following "(.*)":')
def given_i_have_the_following_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And I have the following "(.*)" models:')
def and_i_have_the_following_group1_models(step, group1):
    assert False, 'This step must be implemented'


@step(u'When I add them to the section')
def when_i_add_them_to_the_section(step):
    assert False, 'This step must be implemented'


@step(u'And I start monitoring the number of queries run')
def and_i_start_monitoring_the_number_of_queries_run(step):
    assert False, 'This step must be implemented'


@step(u'Then both will be contained in the "(.*)" on the section')
def then_both_will_be_contained_in_the_group1_on_the_section(step, group1):
    assert False, 'This step must be implemented'


@step(u'Then all three will be contained in the "(.*)" on the section')
def all_three_will_be_contained_in_the_group1_on_the_section(step, group1):
    assert False, 'This step must be implemented'


@step(u'And only 2 query should have been run')
def and_only_2_query_should_have_been_run(step):
    assert False, 'This step must be implemented'
