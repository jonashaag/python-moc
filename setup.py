# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='moc',
    description='Music On Console Python interface',
    long_description=__doc__,
    version='0.1',
    author='Jonas Haag',
    author_email='jonas@lophus.org',
    url='http://moc.lophus.org',
    license='BSD',
    packages=find_packages(),
    include_package_data=True
)
