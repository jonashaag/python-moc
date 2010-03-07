.. Python Music On Console documentation master file, created by
   sphinx-quickstart on Sat Mar  6 21:43:05 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Music On Console
=======================
*Python Music On Console* is a wrapper over the amazing console music player
moc_. It currently consist of two modules:

.. _moc: http://moc.daper.net

A mocp Python interface
-----------------------
The :mod:`moc` wraps the ``mocp`` console interface and provides
an API to all actions listed in ``mocp --help``.

.. toctree::
   :maxdepth: 3

   moc


An event system based on the interface
--------------------------------------
The :mod:`mocevent` module is a tiny and dynamic event system based on
the :mod:`moc` module. It makes you able to execute callbacks when moc
changed for instance the currently played track.

.. toctree::
   :maxdepth: 3

   mocevent
   usage examples <examples>

