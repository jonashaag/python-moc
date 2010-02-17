#
#     This file is part of 'python-moc', a Python music on console interface.
#     Copyright (c) 2010 Jonas Haag <jonas@lophus.org>.
#     All rights reserved. See LICENSE for licensing information.
#
"""
    python-moc, a Python music on console interface
    ===============================================
    python-moc provides a small wrapper over moc's console output. Mainly,
    it converts the output acquired by
        mocp --info
    to a Python dict. It also does some normalization on keys/values.

    It can be used as follows:

        >>> moc.get_state()
        -1                          # apparently moc is not running, so
        >>> moc.get_info_dict()     # no output here
        >>> moc.get_state()         # I started moc, but it's stopped
        0
        >>> moc.get_info_dict()
        {'state': 0}
        >>> moc.get_state()         # I started playing a file
        2
        >>> moc.get_info_dict()
        {'album': 'Whoracle',
         'artist': 'In Flames',
         'avgbitrate': '320kbps',
         'bitrate': '320kbps',
         'currentsec': '10',
         'currenttime': '00:10',
         'file': '../In Flames/Whoracle/In Flames - The Hive.mp3',
         'rate': '44kHz',
         'songtitle': 'The Hive',
         'state': 2,
         'timeleft': '03:53',
         'title': '5 In Flames - The Hive (Whoracle)',
         'totalsec': '243',
         'totaltime': '04:03'}

"""
import os

MOC_COMMAND = 'mocp --info 2>/dev/null'
# The shell command that gets us the information

STATE_NOT_RUNNING = -1
STATE_STOPPED = 0
STATE_PAUSED  = 1
STATE_PLAYING = 2

STATES = {
    'PLAY'  : STATE_PLAYING,
    'STOP'  : STATE_STOPPED,
    'PAUSE' : STATE_PAUSED
}

def _get_moc_info():
    """ Calls ``MOC_COMMAND`` and returns its output. """
    return os.popen(MOC_COMMAND).read()

def _moc_output_to_dict(output):
    """
    Converts the given moc ``output`` into a dictonary. If the output is empty,
    return ``None`` instead.

    The conversion works as follows:
        For each line:
            split the line on first match of a ":"
            where the first part of the result is the key and the second part
            is the value.
            lowercase the key and add the key/value to the dict.
    """
    if not output:
        return
    return dict((key.lower(), value[1:]) for key, value in
                (line.split(':', 1) for line in output.strip('\n').split('\n')))

def get_info_dict():
    """
    Returns a dictionary with current moc information.

    Gets the dictionary from calling ``moc_output_to_dict`` on the output
    acquired using ``get_moc_info``, converts the 'state' given in this dict
    to one of ``STATE_STOPPED``, ``STATE_PAUSED`` or ``STATE_PLAYING`` and
    returns the dict.
    """
    dct = _moc_output_to_dict(_get_moc_info())
    if dct is None:
        return
    dct['state'] = STATES[dct.pop('state')]
    return dct

def get_state():
    """
    Returns the current state of moc.

    (``STATE_STOPPED``, ``STATE_PAUSED`` or  ``STATE_PLAYING``)
    """
    try:
        return get_info_dict()['state']
    except TypeError:
        return STATE_NOT_RUNNING

def is_paused():
    """ Returns ``True`` if moc is currently paused. """
    return get_state() == STATE_PAUSED

def is_playing():
    """ Returns `` True`` if moc is currently in playing state. """
    return get_state() == STATE_PLAYING

def is_stopped():
    """ Returns ``True`` if moc is currently stopped. """
    return get_state() == STATE_STOPPED
