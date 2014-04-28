armstrong.core.arm_sections
===========================
Provides content categorization within an Armstrong site.

The ``Section`` model provides hierarchical organization for content, or
really for anything you'd like to organize. In the Armstrong ecosystem
we organize articles. For example, the Texas Tribune has an Immigration
section which in turn has Sanctuary Cities and Dream Act as children
sections. Like a typical tree structure, anything belonging to a child
also belongs to the parent. You can also ignore the hierarchy and create
a flat structure.

ArmSections also provides a basic View for items in a section and a template
tag for displaying (and linking to) all the sections. Also available is a
Feed view, an Admin display mixin and a queryset manager for use on the
content items. These aren't documented as they should be...


Usage
-----
Add a ``section`` field to any model that you would like to show up
in a given section. ::

    # models.py
    from django.db import models
    from armstrong.core.arm_sections.models import Section

    class MyArticle(models.Model):
        title = models.CharField(max_length=100)
        body = models.TextField()
        section = models.ForeignKey(Section)

You can also relate to multiple sections through a ``ManyToManyField``::

    class MyArticle(models.Model):
        sections = models.ManyToManyField(Section)

Sections are designed to hold items of a single model type (or a single
parent type, inheritance is fine. Actually inheritance is one of ArmSections'
strengths). If you aren't using the ``armstrong.apps.content`` companion
package, you'll need to set ``ARMSTRONG_SECTION_ITEM_MODEL`` in settings.

On the other side of the relationship, Sections have ``items`` and
``published`` attributes that allow different access to the associated
content. These attributes are powered by configurable backends for
flexibility so you can tailor the lookup. For example, "published" might
mean a non-draft flag on the content or a combination of flag and date;
swap the ``published`` backend to meet the need.

``ItemFilter`` and ``PublishedItemFilter`` are the defaults and tie into
`managers`_ used in the companion (but not required)
`armstrong.core.arm_content`_. They also know about `django-model-utils`_
InheritanceManager and will utilize ``select_subclasses()`` if available.


.. _managers: https://docs.djangoproject.com/en/1.6/topics/db/managers/
.. _armstrong.core.arm_content: https://github.com/armstrong/armstrong.core.arm_content
.. _django-model-utils: https://github.com/carljm/django-model-utils


.. Pull this next sub-section into real documentation and expand it

Displaying Sections
"""""""""""""""""""
You can display a section through the ``SimpleSectionView`` class-based-view
(CBV). First, setup a named URL route::

    url(r'^section/(?P<full_slug>[-\w/]+)',
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),

Then use the ``{% section_menu %}`` template tag to display a list of all
sections inside your template. ``{% load section_helpers %}`` first to use the
template tag and provide a ``section_view`` kwarg that is the named URL route
associated with your section view. Putting it together::

    {% load section_helpers %}
    {% section_menu section_view='section_view' %}

With the following sections in your database... ::

    Politics
    Sports
        Football
        Basketball
    Fashion

...and the example so far, the output from your template would look like this::

    <ul class="root">
        <li>
            <a href='/section/politics/'>Politics</a>
        </li>
        <li>
            <a href='/section/sports/'>Sports</a>
            <ul class="children">
                <li>
                    <a href='/section/sports/football/'>Football</a>
                </li>
                <li>
                    <a href='/section/sports/basketball/'>Basketball</a>
                </li>
            </ul>
        </li>
        <li>
            <a href='/section/fashion/'>Fashion</a>
        </li>
    </ul>


Installation & Configuration
----------------------------
#. ``pip install armstrong.core.arm_sections``

#. Add ``armstrong.core.arm_sections`` to your ``INSTALLED_APPS``

**Optional Settings:** (Used in ``settings.py``)

There are three settings that you can use to change the behavior of this
component and its relation to content items.

``ARMSTRONG_SECTION_ITEM_BACKEND``
    This is used to configure which backend is used to find the items
    associated with a given ``Section``. (default:
    ``armstrong.core.arm_sections.backend.ItemFilter``)

``ARMSTRONG_SECTION_PUBLISHED_BACKEND``
    Same as ITEM_BACKEND except it is designed for limiting to published items.
    (default: ``armstrong.core.arm_sections.backend.PublishedItemFilter``)

``ARMSTRONG_SECTION_ITEM_MODEL``
    Used by the two default backends to determine which model has a section
    associated with it. (default: ``armstrong.apps.content.models.Content``)


Contributing
------------
Development occurs on Github. Participation is welcome!

* Found a bug? File it on `Github Issues`_. Include as much detail as you
  can and make sure to list the specific component since we use a centralized,
  project-wide issue tracker.
* Testing? ``pip install tox`` and run ``tox``
* Have code to submit? Fork the repo, consolidate your changes on a topic
  branch and create a `pull request`_. The `armstrong.dev`_ package provides
  tools for testing, coverage and South migration as well as making it very
  easy to run a full Django environment with this component's settings.
* Questions, need help, discussion? Use our `Google Group`_ mailing list.

.. _Github Issues: https://github.com/armstrong/armstrong/issues
.. _pull request: http://help.github.com/pull-requests/
.. _armstrong.dev: https://github.com/armstrong/armstrong.dev
.. _Google Group: http://groups.google.com/group/armstrongcms


State of Project
----------------
`Armstrong`_ is an open-source news platform that is freely available to any
organization. It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_ and a grant from the `John S. and James L. Knight
Foundation`_. Armstrong is available as a complete bundle and as individual,
stand-alone components.

.. _Armstrong: http://www.armstrongcms.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
