#
#     This file is part of 'python-moc', a Python music on console interface.
#     Copyright (c) 2010 Jonas Haag <jonas@lophus.org>.
#     All rights reserved. See LICENSE for licensing information.
#
"""
    mocevent - a tiny event system layer on top of the moc library
    ==============================================================
    *mocevent* is a small library aiming to provide a simple but flexible
    event system for music on console using the python-moc library.

    With *mocevent*, you can bind Python functions to events like *'song-changed'*
    or *'moc-started'*. For example, if you want a callback function be called
    whenever moc changes the currently played song, do it with this few lines:

        >>> import mocevent
        >>> @mocevent.register('song-changed')
        ... def my_song_changed_callback(info_dict):
        ...     print "Song has changed to %s" % info_dict['songtitle']

        >>> mocevent.mainloop()

    mocevent now checks every second whether the song has changed, and if it
    has, it calls the given callback function with the info dictionary known
    from the *python-moc* library.

    Of course you can define your own events using *mocevent*. Let's say you
    want to have an event called *'in-flames-song-started'* that is invoked, as
    the name says, whenever moc plays a song from the great Melodic Death Metal
    band In Flames.

        >>> @mocevent.listener('in-flames-song-started')
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
        >>> @mocevent.register('in-flames-song-started')
        ... def callback(info_dict):
        ...     print "You're now listening to %s by In Flames! :-)" % info_dict['songtitle']
"""
import time
from collections import defaultdict
import moc

EVENT_CALLBACKS = defaultdict(list)
LISTENERS = list()

def register(event_name, callback=None):
    """
    Decorator used to register a callback for `event_name`.

    Aliases: ``register``, ``register_callback``
    """
    if callback is not None:
        EVENT_CALLBACKS[event_name].append(callback)
        return callback
    else:
        def wrapper(callback):
            EVENT_CALLBACKS[event_name].append(callback)
            return callback
        return wrapper
register_callback = register

def emit_event(event_name, *args, **kwargs):
    for callback in EVENT_CALLBACKS.get(event_name, ()):
        callback(*args, **kwargs)

def listener(event, listen_closed=False):
    def wrapper(func):
        LISTENERS.append(func)
        func.garage = dict()
        func.event = event
        func.listen_closed = listen_closed
        return func
    return wrapper


@listener('song-changed')
def song_changed_listener(garage, info_dict):
    old_song = garage.get('file', None)
    garage['file'] = info_dict.get('file', None)
    if old_song is None:
        return True
    try:
        return info_dict['file'] != old_song
    except KeyError:
        # rare, but happens
        return False

@listener('state-changed')
def state_changed_listener(garage, info_dict):
    old_state = garage.get('state', None)
    garage['state'] = info_dict['state']
    if old_state is None:
        return True
    return info_dict['state'] != old_state

@listener('moc-closed', listen_closed=True)
def moc_quitted_listener(garage, info_dict):
    was_quitted_before = garage.get('quitted', None)
    garage['quitted'] = info_dict is None
    return was_quitted_before is False and info_dict is None

@listener('moc-started', listen_closed=True)
def moc_started_listener(garage, info_dict):
    was_started_before = garage.get('started', None)
    garage['started'] = info_dict is not None
    return was_started_before is False and info_dict is not None


def mainloop(refresh_interval=1):
    """
    Runs the *mocevent* mainloop.

    This loop checks every `refresh_interval` seconds whether some event has
    happened and invokes the callbacks for that event in that case.
    """
    while True:
        info_dict = moc.get_info_dict()
        for listener_ in LISTENERS:
            if info_dict is None and not listener_.listen_closed:
                continue
            if listener_(listener_.garage, info_dict):
                emit_event(listener_.event, info_dict)
        time.sleep(refresh_interval)

if __name__ == '__main__':
    mainloop()
