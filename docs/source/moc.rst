python-moc, a Python music on console interface
===============================================
*python-moc* provides a small wrapper over moc's command-line interface.

It makes all features like playing and enqueuing files and playlist, controlling the playback and getting information about the currently played track available via Python.

.. module:: moc

Most interesting functions
--------------------------
.. autofunction:: moc.get_info_dict
.. autofunction:: moc.quickplay


Getting information about the current playback state
----------------------------------------------------
.. autofunction:: moc.get_state
.. autofunction:: moc.is_playing
.. autofunction:: moc.is_paused
.. autofunction:: moc.is_stopped


Controlling the playback
------------------------
.. autofunction:: moc.play
.. autofunction:: moc.pause
.. autofunction:: moc.unpause
.. autofunction:: moc.toggle_playback
.. autofunction:: moc.stop

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


Working with playlists
----------------------
.. autofunction:: playlist_append
.. autofunction:: playlist_clear


Various other functions
-----------------------
.. autofunction:: increase_volume
.. autofunction:: decrease_volume
.. autofunction:: seek
.. autofunction:: moc.get_info_dict
.. autofunction:: moc.quickplay


Controlling the server
----------------------
.. autofunction:: start_server
.. autofunction:: shutdown_server
