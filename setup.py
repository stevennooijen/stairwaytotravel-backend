import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="stairway",
    description="Stairway to Travel backend utilities.",
    author="Steven Nooijen",
    packages=find_packages('stairway'),
    package_dir={"": "stairway"},
    long_description=read('README.md'),
)
