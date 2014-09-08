CHANGES
=======

1.6.0 (2014-09-07)
------------------

- Support for Django 1.5, 1.6, 1.7

- **DEPRECATION:** deprecate ``SectionTreeAdminMixin``. Use the MPTT fields
  TreeForeignKey/TreeOneToOneField/TreeManyToManyField explicitly on the model.

- **DEPRECATION:** ``get_query_set()`` will be removed for Django 1.6+ in
  ArmSections 2.0. Follow Django's paradigm and use ``get_queryset()`` instead.

- New ``BaseSection`` abstract model for easier subclassing

- Section ``slug`` length is now 200 characters (up from 50)

- Section ``full_slug`` is now unique, which is how we always treated it anyway

- Improved default Section ordering (by title instead of random)

- South migrations are moved to ``south_migrations/`` and older Django's should
  upgrade to South 1.0

- Use Setuptools and pkg_resources for namespacing

- Development: use ArmDev 2.0

- Development: added Tox testing config

- Stop shipping tests and move them out of the component module

- Test and coverage improvements
