# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='mocp',
    version='0.3.0',
    description='A Python library to control the MOC (music on console) audio player for Linux',
    author='Jonas Haag, Ken',
    author_email='kenjyco@gmail.com',
    license='BSD',
    url='https://github.com/kenjyco/mocp',
    download_url='https://github.com/kenjyco/mocp/tarball/v0.3.0',
    packages=find_packages(),
    include_package_data=True,
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
