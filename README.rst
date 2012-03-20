armstrong.core.arm_sections
===========================
Provides the basic concept of sections within an Armstrong site.

You can use ``Section`` models to organize your content into a group.  Sections
can have a parent section to allow you to create a hierarchy.  For example, the
`Texas Tribune`_ has an Immigration section which in turns has Sanctuary Cities
and Dream Act as children sections.

You are not limited to a hierarchical structure---you can create a flat
structure as well.


Usage
-----
You need to add a ``section`` field to any model that you would like to show up
in a given section.  For example::

    # your models.py
    from django.db import models
    from armstrong.core.arm_sections.models import Section


    class MyArticle(models.Model):
        title = models.CharField(max_length=100)
        body = models.TextField()

        section = models.ForeignKey(Section)

You can also relate to multiple sections as well through a ``ManyToManyField``:

::

    class MyArticle(models.Model):
        # other fields
        sections = models.ManyToManyField(Section)


.. Pull this next sub-section into real documentation and expand it

Displaying Sections
"""""""""""""""""""
You can display a section through the ``SimpleSectionView`` class-based-view
(CBV).  The standard project template in Armstrong provides an example of how
to configure this view.

::

    url(r'^section/(?P<full_slug>[-\w/]+)',
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),


You can use the ``{% section menu %}`` template tag to display list of all
sections inside your template.  You must load the ``section_helpers`` template
tags to use this.  You must provide it with a ``section_view`` kwarg that is
associated with the section view you configure inside your URL routes.  For
example, to display a list of sections that link to the section view created
above, you would put this in your template.

::

    {% load section_helpers %}
    {% section_menu section_view='section_view' %}

With the following sections in your database:

::

    Politics
    Sports
        Football
        Basketball
    Fashion

Using all of the example we have so far, the output from your template would
look like this:

::

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
We recommend installing this through the Cheese Shop.

::

    pip install armstrong.core.arm_sections

This gets you the latest released version of ``armstrong.core.arm_sections``.

Configuration
"""""""""""""
There are two setting that you can use to change the behavior of this
component.

``ARMSTRONG_SECTION_ITEM_BACKEND``
    This is used to configure which backend is used to find the items
    associated with a given ``Section``.  (default:
    ``armstrong.core.arm_sections.backend.ItemFilter``)

``ARMSTRONG_SECTION_ITEM_MODEL``
    This is used by the default ``find_related_models`` backend to determine
    which model has a section associated with it. (default:
    ``armstrong.apps.content.models.Content``)


Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `pull request`_


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_, and a grant from the `John S. and James L. Knight
Foundation`_.

To follow development, be sure to join the `Google Group`_.

``armstrong.core.arm_section`` is part of the `Armstrong`_ project.  You're
probably looking for that.


License
-------
Copyright 2011 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _Armstrong: http://www.armstrongcms.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _Google Group: http://groups.google.com/group/armstrongcms
.. _pull request: http://help.github.com/pull-requests/
.. _Fork it: http://help.github.com/forking/
