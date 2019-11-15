import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="stairway",
    description="Stairway to Travel backend utilities.",
    author="Steven Nooijen",
    # Alternatively use find_packages('.') and exclude folders
    packages=find_packages('src'),
    package_dir={"": "src"},
    long_description=read('README.md'),
)
