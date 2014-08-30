# Nothing in this file should need to be edited.
#   Use package.json to adjust metadata about this package.
#   Use MANIFEST.in to include package-specific data files.
import os
import json
from setuptools import setup, find_packages


info = json.load(open("./package.json"))


def generate_namespaces(package):
    i = package.count(".")
    while i:
        yield package.rsplit(".", i)[0]
        i -= 1
NAMESPACE_PACKAGES = list(generate_namespaces(info['name']))

if os.path.exists("MANIFEST"):
    os.unlink("MANIFEST")

setup_kwargs = {
    "author": "Bay Citizen & Texas Tribune",
    "author_email": "dev@armstrongcms.org",
    "url": "http://github.com/armstrong/%s/" % info["name"],
    "packages": find_packages(),
    "namespace_packages": NAMESPACE_PACKAGES,
    "include_package_data": True,
    "classifiers": [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
}

setup_kwargs.update(info)
setup(**setup_kwargs)
