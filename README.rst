mocp
====

A Python library to control the MOC (music on console) audio player for
Linux.

    Note: The `actual player <https://moc.daper.net/>`__ must be
    installed on the system (i.e. ``sudo apt-get install moc``).

Install
^^^^^^^

::

    % pip install mocp

Use
^^^

::

    % ipython
    ...

    In [1]: import moc

    In [2]: moc.find_and_play('~/music-dir/blah*')

    In [3]: moc.go('12:15')         # jump to particular point in current track

    In [4]: moc.go('1h23m12s')      # jump to particular point in current track

    In [5]: moc.go(500)             # jump to particular point in current track

    In [6]: moc.info_string()
    Out[6]: '08:21 (501) of 95:35 into /home/user/music-dir/blah-thing/file.mp3'
