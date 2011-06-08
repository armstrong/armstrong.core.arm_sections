Items and Backends
==================

Sections provide a property called ``items`` which allow you to access all of
the items associated with them.  ``items`` is powered by backends so it can
look at the most efficient place to figure out how to get what is associated
with it.

``items`` is powered by a callable backend.  It's up to the backend to figure
out how what models it should return.


``find_related_models``
-----------------------

``find_related_models`` is the default backend for handling requests to a
``Section``'s ``items`` property.  It queries the configured model looking for
related data.  It uses the model specified in ``ARMSTRONG_SECTION_ITEM_MODEL``
to search for data.

For this to work across multiple models this assumes you are using a
non-abstract model as the a base ``Content`` model with specific types
extending from that.  This is the style that Armstrong uses for it's content.

``find_related_models`` knows about the ``InheritanceManager`` in
`django-model-util`_ and attempts to utilize ``select_subclasses``.  That
limits the number of queries to the database to one.

.. _django-model-utils: https://github.com/carljm/django-model-utils

Creating custom backends
------------------------
You can change which backend is used by changing the
``ARMSTRONG_SECTION_ITEM_BACKEND`` value in your Django settings.  For example,
the default setting is::

    ARMSTRONG_SECTION_ITEM_BACKEND = 'armstrong.core.arm_sections.backends.find_related_models'

You should include the full path to the callable.  The custom backend is
provided one argument, the ``section`` that was used to call it.  It should
return an iterable object.  You *can* return a ``QuerySet``, but that is not
currently a requirement.
