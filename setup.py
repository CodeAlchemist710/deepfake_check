"""
Setup script for deepfake_check package.
"""

from setuptools import setup, find_packages

setup(
    name="deepfake_check",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
