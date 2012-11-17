:mod:`moc.event` - a tiny event system layer on top of the moc library
======================================================================
*moc.event* is a small library aiming to provide a simple but flexible
event system for Music On Console.

With *moc.event*, you can bind Python functions to events like *'song-changed'*
or *'moc-started'*. For example, if you want a callback function be called
whenever moc changes the currently played song, do it with this few lines:

    >>> import moc.event
    >>> @moc.event.register('song-changed')
    ... def my_song_changed_callback(info_dict):
    ...     print "Song has changed to %s" % info_dict['songtitle']

    >>> moc.event.mainloop()

*moc.event* now checks every second whether the song has changed, and if it
has, it calls the given callback function with the info dictionary known
from the *moc* library.

Of course you can define your own events using *moc.event*. Let's say you
want to have an event called *'in-flames-song-started'* that is invoked, as
the name says, whenever moc plays a song from the great Melodic Death Metal
band In Flames.

    >>> @moc.event.listener('in-flames-song-started')
    ... def in_flames_song_started_listener(garage, info_dict):
    ...     previous_song = garage.get('prevsong', None)
    ...     garage['prevsong'] = info_dict['file']
    ...     if previous_song == info_dict['file']:
    ...         # moc is still playing the same file it did when we checked
    ...         # the last time, so don't emit anything. Just do nothing.
    ...         return
    ...     if previous_song and info_dict['artist'] == 'In Flames':
    ...         # moc is not playing the old file any more, and the played
    ...         # file is from In Flames, so emit the event: return ``True``
    ...         return True

.. todo::
   Maybe describe the code?

Now we can register callbacks for that event:
    >>> @moc.event.register('in-flames-song-started')
    ... def callback(info_dict):
    ...     print "You're now listening to %s by In Flames! :-)" % info_dict['songtitle']


Examples
--------
Basic example
~~~~~~~~~~~~~
.. literalinclude:: ../../examples/event_example.py
   :linenos:
   :language: python

LastFM scrobbler
~~~~~~~~~~~~~~~~
.. literalinclude:: ../../examples/lastfmsubmit.py
   :linenos:
   :language: python
