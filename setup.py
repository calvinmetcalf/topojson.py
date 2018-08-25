import io
import os
import re
from setuptools import setup, find_packages


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(path):
    content = read(path)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


DESCRIPTION = "Python topojson toolkit"
LONG_DESCRIPTION = """
topojson.py is a python interface for conversion
between geojson and topojson and topojson simplification.
We will add more topojson-specific operations in the future.
"""
NAME = "topojson"
AUTHOR = "Calvin Metcalf"
MAINTAINER = "Philipp Kats"
MAINTAINER_EMAIL = "casyfill@gmail.com"
URL = 'https://github.com/calvinmetcalf/topojson.py'
LICENSE = 'BSD'
PACKAGES = find_packages()
VERSION = version('pdvega/__init__.py')
DEV_REQUIRES = get_install_requirements("requirements_dev.txt")

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    packages=PACKAGES,
    extras_requires={
        'dev': DEV_REQUIRES
    },
    test_suite="tests",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
)
