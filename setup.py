import platform
import os
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "infi", "unittest", "__version__.py"), "rb") as version_file:
    exec version_file.read()

_REQUIREMENTS = ["pyforge", "bunch"]
if platform.python_version() < '2.7':
    _REQUIREMENTS.append('unittest2')

setup(name="infi.unittest",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.7",
          ],
      description="Unittest extension library",
      #license="Proprietary",
      author="Rotem Yaari",
      author_email="",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      napespace_packages=["infi"],
      install_requires=_REQUIREMENTS,
      scripts=[],
      entry_points = {
            'nose.plugins.0.10': [
                'infi = infi.unittest.nose_plugin:NosePlugin'
                ]
            },
      )
