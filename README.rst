armstrong.core.arm_sections
===========================
Provides the basic concept of sections within an Armstrong site.

.. warning:: This is development level software.  Please do not unless you are
             familiar with what that means and are comfortable using that type
             of software.

Sections give you a way to organize your content into logical groups.  Sections
can have a parent section to allow you to create a hierarchy.  For example, the
`Texas Tribune`_ has an Immigration section which in turns has Sanctuary Cities
and Dream Act as children sections.

Of course, you can create a flat infrastructure too if you would like.  Simply
ignore the parent/child features present.  The parent/child relationship is
managed through a `django-mptt`_ using a technique called *modified preordered
tree traversal*.


Installation & Configuration
----------------------------

::

    NAME=armstrong.core.arm_sections
    pip install -e git://github.com/armstrongcms/$NAME.git#egg=$NAME

There are two settings that should be set for sections to work.  Unless you're
using a custom content model, you should be able to use these settings without
tweaking::

    ARMSTRONG_SECTION_ITEM_BACKEND="armstrong.core.arm_sections.backend.find_related_models"
    ARMSTRONG_SECTION_ITEM_MODEL="armstrong.apps.content.models.Content"

.. note:: As of version 0.1.x that shipped with Armstrong 11.06, these settings
          are required.  Future versions of armstrong.core.arm_sections will
          have these both set by default.


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

You can also relate to multiple sections as well through a ``ManyToManyField``.

To display a section view, we provide the ``SimpleSectionView``. An example is
provided in the demo project which has the following in ``urls.py``::

    url(r'^section/(?P<full_slug>[-\w/]+)',
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),
    # renders the view identified by full_slug using section.html

A template tag to render menus is provided called ``section_menu``. It can be
customized by passing in a template, but standard usage looks like::

    {% load section_helpers %}
    {% section_menu section_view='section_view' %}

The ``section_view`` parameter tells ``section_menu`` what view to link to for
a given section. If your urls.py is configured as in the above example, the
menu will render as::

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
Foundation`_.  The first stable release is scheduled for September, 2011.

To follow development, be sure to join the `Google Group`_.

``armstrong.core.arm_content`` is part of the `Armstrong`_ project.  You're
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
.. _django-mptt: https://github.com/django-mptt/django-mptt
