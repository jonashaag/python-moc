:mod:`moc`: Wrapper around `mocp`
=================================
The :mod:`moc` package wraps the ``mocp`` console interface and provides
an API to all actions listed in ``mocp --help``.

.. module:: moc

Controlling the server
----------------------
.. autofunction:: start_server
.. autofunction:: stop_server

Controlling the playback
------------------------
.. autofunction:: moc.quickplay
.. autofunction:: moc.pause
.. autofunction:: moc.unpause
.. autofunction:: moc.toggle_playback
.. autofunction:: moc.stop
.. autofunction:: moc.play
.. autofunction:: seek

.. autofunction:: increase_volume
.. autofunction:: decrease_volume

.. autofunction:: moc.next
.. autofunction:: moc.previous

.. autofunction:: enable_repeat
.. autofunction:: disable_repeat
.. autofunction:: toggle_repeat

.. autofunction:: enable_shuffle
.. autofunction:: disable_shuffle
.. autofunction:: toggle_shuffle

.. autofunction:: enable_autonext
.. autofunction:: disable_autonext
.. autofunction:: toggle_autonext

Getting information about the current playback
----------------------------------------------
.. autofunction:: moc.get_info_dict
.. autofunction:: moc.get_state
.. autofunction:: moc.is_playing
.. autofunction:: moc.is_paused
.. autofunction:: moc.is_stopped

Working with playlists
----------------------
.. autofunction:: playlist_get
.. autofunction:: playlist_append
.. autofunction:: playlist_clear
