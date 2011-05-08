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


Getting Items in a Section
""""""""""""""""""""""""""

Sections provide a property called ``items`` which allow you to access all of
the items associated with them.  ``items`` is powered by a backend
infrastructure so it can look at the most efficient place to figure out how to
get what is associated with it.

The easiest to set up is the standard database-powered QuerySet.  The default
one is configurable by the following settings::

    ARMSTRONG_SECTIONS_QUERYSET_BACKEND = {
        "_default": "myapp.models.SomeModel",
        "immigration": "other.models.SomeOtherModel",
    }

By default, this loads the ``objects`` property on this model and attempts to
call ``by_section(<section.slug>)`` to determine which models are available
for the given section.

*Note*: There are plans for providing additional backends by default.

Installation
------------

::

    pip install -e git://github.com/armstrongcms/armstrong.core.arm_sections


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
Foundation`_.  The first release is scheduled for June, 2011.

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
