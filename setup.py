from distutils.core import setup

from setuptools import find_packages

setup(
    name="or-anonymizer",
    version="0.1.0a",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    description="A Python module that provides multiple anonymization techniques for text.",
    long_description=open("README.md").read(),
    install_requires=["pydantic==1.6.1", "numpy==1.19.1", "python-dateutil==2.8.1"],
)
