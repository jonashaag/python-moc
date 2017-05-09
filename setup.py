# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.rst', 'r') as fp:
    long_description = fp.read()

setup(
    name='mocp',
    version='0.3.3',
    description='A Python library to control the MOC (music on console) audio player',
    long_description=long_description,
    author='Jonas Haag, Ken',
    author_email='kenjyco@gmail.com',
    license='BSD',
    url='https://github.com/kenjyco/mocp',
    download_url='https://github.com/kenjyco/mocp/tarball/v0.3.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'input-helper',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Intended Audience :: Developers',
    ],
    keywords = ['moc', 'mocp', 'console audio', 'mp3 player']
)
