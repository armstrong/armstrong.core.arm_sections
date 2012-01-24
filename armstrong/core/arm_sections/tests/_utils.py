from datetime import datetime
from django.core.files import File
from django.conf import settings

from armstrong.dev.tests.utils import ArmstrongTestCase
from armstrong.dev.tests.utils.concrete import *
from armstrong.dev.tests.utils.users import *

from ..models import Section

import fudge


class ArmSectionsTestCase(ArmstrongTestCase):
    def setUp(self):
        super(ArmSectionsTestCase, self).setUp()
        self.sections = []
        data = [
                ('Local', 'local', 'All about local', None),
                ('Sports', 'sports', 'All about sports', None),
                ('College', 'college', 'All about college sports', 1),
                ('Pro', 'pro', 'All about pro sports', 1),
                ('Weather', 'weather', 'All about weather', None),
                ]
        for title, slug, summary, parent in data:
            if parent is not None:
                parent = self.sections[parent]
            self.sections.append(Section.objects.create(
                    title=title,
                    slug=slug,
                    summary=summary,
                    parent=parent,
                ))


# From django.conf.__init__ and django.test.utils.
# https://github.com/django/django/tree/5acd91d3ec80021d6c8fc25aab3b21098b1e8322
#
# TODO: Move this to armstrong.dev.tests.utils.

class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    def __setattr__(self, name, value):
        if name in ("MEDIA_URL", "STATIC_URL") and value and not value.endswith('/'):
            warnings.warn("If set, %s must end with a slash" % name,
                          DeprecationWarning)
        elif name == "ADMIN_MEDIA_PREFIX":
            warnings.warn("The ADMIN_MEDIA_PREFIX setting has been removed; "
                          "use STATIC_URL instead.", DeprecationWarning)
        object.__setattr__(self, name, value)

class UserSettingsHolder(BaseSettings):
    """
    Holder for user configured settings.
    """
    # SETTINGS_MODULE doesn't make much sense in the manually configured
    # (standalone) case.
    SETTINGS_MODULE = None

    def __init__(self, default_settings):
        """
        Requests for configuration variables not in this class are satisfied
        from the module specified in default_settings (if possible).
        """
        self.default_settings = default_settings

    def __getattr__(self, name):
        return getattr(self.default_settings, name)

    def __dir__(self):
        return self.__dict__.keys() + dir(self.default_settings)

    # For Python < 2.6:
    __members__ = property(lambda self: self.__dir__())


class OverrideSettingsHolder(UserSettingsHolder):
    pass


class override_settings(object):
    """
    Acts as either a decorator, or a context manager. If it's a decorator it
    takes a function and returns a wrapped function. If it's a contextmanager
    it's used with the ``with`` statement. In either event entering/exiting
    are called before and after, respectively, the function/block is executed.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.wrapped = settings._wrapped

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        from django.test import TransactionTestCase
        if isinstance(test_func, type) and issubclass(test_func, TransactionTestCase):
            original_pre_setup = test_func._pre_setup
            original_post_teardown = test_func._post_teardown
            def _pre_setup(innerself):
                self.enable()
                original_pre_setup(innerself)
            def _post_teardown(innerself):
                original_post_teardown(innerself)
                self.disable()
            test_func._pre_setup = _pre_setup
            test_func._post_teardown = _post_teardown
            return test_func
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def enable(self):
        override = OverrideSettingsHolder(settings._wrapped)
        for key, new_value in self.options.items():
            setattr(override, key, new_value)
        settings._wrapped = override

    def disable(self):
        settings._wrapped = self.wrapped
