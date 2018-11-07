import os
import sys
import platform
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "infi", "unittest", "__version__.py"), "rb") as version_file:
    exec(version_file.read())

_REQUIREMENTS = ["pyforge", "munch"]
if sys.version_info < (2, 7):
    _REQUIREMENTS.append('unittest2')


setup(name="infi.unittest",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Programming Language :: Python"
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.5",
          ],
      description="Unittest extension library",
      license="BSD",
      author="Rotem Yaari",
      author_email="",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      namespace_packages=["infi"],
      install_requires=_REQUIREMENTS,
      scripts=[],
      entry_points = {
            'nose.plugins.0.10': [
                'infi = infi.unittest.nose_plugin:NosePlugin'
                ]
            },
      )
