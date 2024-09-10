
from setuptools import setup
from setuptools.command.install import install
import os


class CustomInstallCommand(install):
    def run(self):
        install.run(self)

setup(
    name="django-blog",
    version="0.1",
    packages=["django_blog"],
    cmdclass={'install': CustomInstallCommand},
)
