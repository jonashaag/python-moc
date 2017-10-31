Install
-------

Install the actual `MOC player/server <https://moc.daper.net/>`__

::

    % sudo apt-get install -y moc

    or

    % brew install moc
    % jackd -d coreaudio

..

    Note: if using a Mac, you need to run
    `jack <http://www.jackaudio.org/>`__ in another terminal EVERY TIME
    (i.e. ``jackd -d coreaudio``).

Verify that the MOC server can start

::

    % mocp

..

    Press ``q`` to quit.

Install with ``pip``

::

    % pip3 install mocp

Usage
-----

.. code:: python

    In [1]: import moc

    In [2]: moc.find_and_play('~/music-dir/blah*')

    In [3]: moc.go('12:15')         # jump to particular point in current track

    In [4]: moc.go('1h23m12s')      # jump to particular point in current track

    In [5]: moc.go(500)             # jump to particular point in current track

    In [6]: moc.info_string()
    Out[6]: '08:21 (501) of 95:35 into /home/user/music-dir/blah-thing/file.mp3'
