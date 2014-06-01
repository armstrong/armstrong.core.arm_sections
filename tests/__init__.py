from unittest import TestSuite


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(loader.loadTestsFromNames([
        'tests.backends',
        'tests.models',
        'tests.template_tags',
        'tests.utils',
        'tests.views',
        'tests.with_section'
    ]))
    return suite
