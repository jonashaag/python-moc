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
def moc_quit_listener(garage, info_dict):
    was_quit_before = garage.get('quit', None)
    garage['quit'] = info_dict is None
    return was_quit_before is False and info_dict is None

@listener('moc-started', listen_closed=True)
def moc_started_listener(garage, info_dict):
    was_started_before = garage.get('started', None)
    garage['started'] = info_dict is not None
    return was_started_before is False and info_dict is not None


def mainloop(refresh_interval=1):
    """
    Runs the *moc.event* mainloop.

    This loop polls every `refresh_interval` seconds to check whether some
    event has happened and invokes the callbacks for that event in that case.
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
