Python Music On Console
=======================
*Python Music On Console* is a wrapper around the amazing console music player
moc_.

It can be used to play and enqueue files and playlists, control playback,
get information about the currently played track, etc.

.. code-block:: python

    >>> moc.start_server()
    >>> moc.quickplay(list_of_files)
    >>> moc.get_info_dict() =>
    {'album'       : 'Whoracle',
     'artist'      : 'In Flames',
     'songtitle'   : 'The Hive',
     'file'        : '.../In Flames/Whoracle/In Flames - The Hive.mp3',
     'timeleft'    : '03:53',
     'totaltime'   : '04:03', ...}

    >>> moc.next()
    >>> moc.pause()
    >>> moc.resume()
    >>> moc.is_playing()
    >>> moc.toggle_shuffle()
    >>> moc.enable_repeat()
    >>> moc.increase_volume(10)
        ...

.. _moc: http://moc.daper.net


API reference
-------------
.. toctree::
   :maxdepth: 3

   moc
   moc.event


Bugs, feature requests and current development version
------------------------------------------------------
*Python Music On Console* uses Github_ as version control system and bug tracker
and so on.

You can get the current development version from Github_ using :command:`git clone`::

    git clone git://github.com/jonashaag/python-moc

Please file bugs and feature requests using the `Github ticket system`_.

I'm glad to get any kind of feedback! (critique, thanks, ideas, feature requests, blah)

.. _Github: http://github.com/jonashaag/python-moc
.. _Github ticket system: http://github.com/jonashaag/python-moc/issues
